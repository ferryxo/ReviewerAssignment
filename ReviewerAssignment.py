from flask import Flask
import random
import flask
import json

app = Flask(__name__)




def assign_reviews_random(submissions, reviewers, max_n_review):
    submission_reviewers_map = {}
    reviewers_task_map = {}
    n_reviewer = len(reviewers)

    if max_n_review < n_reviewer:
        random.shuffle(reviewers)

        reviewer_index = -1
        for i in range(0, max_n_review):
            for j in range(0, len(submissions)):

                while True:
                    reviewer_index = (reviewer_index + 1) % n_reviewer
                    if reviewers[reviewer_index]['reviewer_id'] in submissions[j]['conflicts']:
                        print 'skip conflict'
                    elif reviewers[reviewer_index] in submission_reviewers_map[submissions[j]['submission_id']]:
                        print 'skip redundant'
                    #elif not submissions[j]['submission_id'] in submission_reviewers_map.keys():
                    #    break
                    else:
                        break


                if submissions[j]['submission_id'] in submission_reviewers_map.keys():
                    submission_reviewers_map[submissions[j]['submission_id']].append(reviewers[reviewer_index])
                else:
                    submission_reviewers_map[submissions[j]['submission_id']] = [reviewers[reviewer_index]]

                if reviewers[reviewer_index]['reviewer_id'] in reviewers_task_map.keys():
                    reviewers_task_map[reviewers[reviewer_index]['reviewer_id']].append(submissions[j])
                else:
                     reviewers_task_map[reviewers[reviewer_index]['reviewer_id']] = [submissions[j]]


    else:
        raise ValueError('number of reviews per submission must be smaller than number of reviewers')


    return flask.jsonify(submissions=submission_reviewers_map, tasks=reviewers_task_map)


def assign_reviews_preference(submissions, reviewers, max_n_review):
    submission_reviewers_map = {}
    reviewers_task_map = {}
    n_reviewer = len(reviewers)

    if max_n_review < n_reviewer:
        random.shuffle(reviewers)


        #distribute reviewers based on their preferences
        for j in range(0, len(submissions)):
            #sequentially find reviewers with preference reviewing this article
            reviewer_index = -1
            reviewer_team = []

            while len(reviewer_team) < max_n_review and reviewer_index < n_reviewer - 1:
                reviewer_index = (reviewer_index + 1)

                reviewer_team = submission_reviewers_map.get(submissions[j]['submission_id'])
                reviewer_team = [] if reviewer_team == None else reviewer_team

                if not submissions[j]['submission_id'] in reviewers[reviewer_index]['preferences']:
                    continue
                elif reviewers[reviewer_index]['reviewer_id'] in submissions[j]['conflicts'] :
                    continue
                #move on if he's already a reviewer for this submission
                elif reviewers[reviewer_index] in reviewer_team:
                    continue

                reviewer_team.append(reviewers[reviewer_index])

                this_reviewer_tasks = reviewers_task_map.get(reviewers[reviewer_index]['reviewer_id'])
                this_reviewer_tasks = [] if this_reviewer_tasks == None else this_reviewer_tasks
                this_reviewer_tasks.append(submissions[j])

                reviewers_task_map[reviewers[reviewer_index]['reviewer_id']] = this_reviewer_tasks

                submission_reviewers_map[submissions[j]['submission_id']] = reviewer_team

        #calculate the avg utilization of each reviewer
        n_avg_task_reviewer = 0
        for tasks in reviewers_task_map.values():
            n_avg_task_reviewer = n_avg_task_reviewer + len(tasks)
        n_avg_task_reviewer = n_avg_task_reviewer/float(len(reviewers_task_map.values()))

        #now distribute the rest of the reviewers to the submission with reviewers less than max_n_review
        for j in range(0, len(submissions)):
            reviewer_index = -1
            reviewer_team = []
            while len(reviewer_team) < max_n_review:
                reviewer_index = (reviewer_index + 1) % n_reviewer

                #check the workload of this reviewer
                this_reviewer_tasks = reviewers_task_map.get(reviewers[reviewer_index]['reviewer_id'])
                this_reviewer_tasks = [] if this_reviewer_tasks == None else this_reviewer_tasks

                #move on if he's already over utilized
                if len (this_reviewer_tasks) > n_avg_task_reviewer:
                    continue
                #move on if he's already a reviewer for this submission
                elif reviewers[reviewer_index] in reviewer_team:
                    continue
                #move on if he's in the conflict list
                elif reviewers[reviewer_index]['reviewer_id'] in submissions[j]['conflicts']:
                    continue

                reviewer_team = submission_reviewers_map.get(submissions[j]['submission_id'])
                reviewer_team = [] if reviewer_team == None else reviewer_team

                reviewer_team.append(reviewers[reviewer_index])
                submission_reviewers_map[submissions[j]['submission_id']] = reviewer_team

                this_reviewer_tasks.append(submissions[j])
                reviewers_task_map[reviewers[reviewer_index]['reviewer_id']] = this_reviewer_tasks



                n_avg_task_reviewer = n_avg_task_reviewer + 1/float(len(reviewers))

    else:
        raise ValueError('number of reviews per submission must be smaller than number of reviewers')


    return flask.jsonify(reviews=submission_reviewers_map, tasks=reviewers_task_map)

@app.route('/')
def hello_world():

    submissions = [{'submission_id':'S00', 'conflicts':['R01']},
                   {'submission_id':'S01', 'conflicts':['R02']},
                   {'submission_id':'S02', 'conflicts':['R04']},
                   {'submission_id':'S03', 'conflicts':['R06']},
                   {'submission_id':'S04', 'conflicts':['R08']}]

    reviewers = [{'reviewer_id':'R00', 'name':'Donald Trump', 'reputation':'0.5', 'preferences':['S00', 'S01']},
                 {'reviewer_id':'R01', 'name':'Hilary Clinton', 'reputation':'0.75', 'preferences':['S01', 'S02']},
                 {'reviewer_id':'R02', 'name':'Bart Simpson', 'reputation':'0.5', 'preferences':['S02', 'S03']},
                 {'reviewer_id':'R03', 'name':'Mickey Mouse', 'reputation':'0.4', 'preferences':['S01']},
                 {'reviewer_id':'R04', 'name':'Minie Mouse', 'reputation':'0.8', 'preferences':['S02']},
                 {'reviewer_id':'R05', 'name':'Oliver Quenn', 'reputation':'0.3', 'preferences':['S02']},
                 {'reviewer_id':'R06', 'name':'Clark Kent', 'reputation':'0.5', 'preferences':['S03']},
                 {'reviewer_id':'R07', 'name':'Bruce Wayne', 'reputation':'0.7', 'preferences':['S03']},
                 {'reviewer_id':'R08', 'name':'Louise Lane', 'reputation':'0.5', 'preferences':['S04']},
                 {'reviewer_id':'R09', 'name':'Lana Lang', 'reputation':'0.9', 'preferences':['S04']}]

    assignment = assign_reviews_preference(submissions, reviewers, 6)
    #assignment = assign_reviews_random(submissions, reviewers, 6)

    return assignment


if __name__ == '__main__':
    app.run()


