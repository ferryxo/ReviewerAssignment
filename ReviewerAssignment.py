from flask import Flask
import random
import flask
import json

app = Flask(__name__)

def assign_review_random(submissions, reviewers, max_n_review):
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
                    elif not submissions[j]['submission_id'] in submission_reviewers_map.keys():
                        break
                    elif reviewers[reviewer_index] in submission_reviewers_map[submissions[j]['submission_id']]:
                        print 'skip redundant'
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

@app.route('/')
def hello_world():

    submissions = [{'submission_id':'S00', 'conflicts':['R00', 'R01']},
                   {'submission_id':'S01', 'conflicts':['R02', 'R03']},
                   {'submission_id':'S02', 'conflicts':['R04', 'R05']},
                   {'submission_id':'S03', 'conflicts':['R06', 'R07']},
                   {'submission_id':'S04', 'conflicts':['R08', 'R09']}]

    reviewers = [{'reviewer_id':'R00', 'name':'Donald Trump', 'reputation':'0.5', 'preference':['S00']},
                 {'reviewer_id':'R01', 'name':'Hilary Clinton', 'reputation':'0.75', 'preference':['S00']},
                 {'reviewer_id':'R02', 'name':'Bart Simpson', 'reputation':'0.5', 'preference':['S01']},
                 {'reviewer_id':'R03', 'name':'Mickey Mouse', 'reputation':'0.4', 'preference':['S01']},
                 {'reviewer_id':'R04', 'name':'Minie Mouse', 'reputation':'0.8', 'preference':['S02']},
                 {'reviewer_id':'R05', 'name':'Oliver Quenn', 'reputation':'0.3', 'preference':['S02']},
                 {'reviewer_id':'R06', 'name':'Clark Kent', 'reputation':'0.5', 'preference':['S03']},
                 {'reviewer_id':'R07', 'name':'Bruce Wayne', 'reputation':'0.7', 'preference':['S03']},
                 {'reviewer_id':'R08', 'name':'Louise Lane', 'reputation':'0.5', 'preference':['S04']},
                 {'reviewer_id':'R09', 'name':'Lana Lang', 'reputation':'0.9', 'preference':['S04']}]

    assignment = assign_review_random(submissions, reviewers, 6)

    return assignment


if __name__ == '__main__':
    app.run()


