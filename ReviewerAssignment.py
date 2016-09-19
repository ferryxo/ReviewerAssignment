from flask import Flask
import random
import flask
import json

app = Flask(__name__)

class Submission:
    def __init__(self, submission_id, team_id):
        self.submission_id = submission_id
        self.team_id = team_id

    def __hash__(self):
        return hash((self.submission_id, self.team_id))

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class Reviewer:
    def __init__(self, user_id, username, reputation, preference):
        self.user_id = user_id
        self.username = username
        self.reputation = reputation
        self.preference = preference

    def __hash__(self):
        return hash((self.user_id, self.username, self.reputation, self.preference))

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def assign_review_random(submissions, reviewers, max_n_review):
    submission_reviewers_map = {}
    reviewers_task_map = {}
    n_reviewer = len(reviewers)

    if max_n_review < n_reviewer:
        random.shuffle(reviewers)

        for i in range(0, len(submissions)):
            review_team = []
            for j in range(i, i+max_n_review):
                reviewer_index = j if j + max_n_review < n_reviewer else j % n_reviewer

                review_team.append(reviewers[reviewer_index].to_JSON())
                if reviewers[reviewer_index].to_JSON() in reviewers_task_map.keys():
                    reviewers_task_map[reviewers[reviewer_index].to_JSON()].append(submissions[i].to_JSON())
                else:
                    this_reviewer_task = [submissions[i].to_JSON()]
                    reviewers_task_map[reviewers[reviewer_index].to_JSON()] = this_reviewer_task

            submission_reviewers_map[submissions[i].to_JSON()] = review_team
    else:
        raise ValueError('number of reviews per submission must be smaller than number of reviewers')


    return flask.jsonify(submissions=submission_reviewers_map, tasks=reviewers_task_map)

@app.route('/')
def hello_world():

    submissions = [Submission('S00', 'T00'),
                   Submission('S01', 'T01'),
                   Submission('S02', 'T02'),
                   Submission('S03', 'T03'),
                   Submission('S04', 'T04'),]

    reviewers = [Reviewer('R00', 'Donald Trump', '0.5', 'S00'),
                 Reviewer('R01', 'Hilary Clinton', '0.75', 'S00'),
                 Reviewer('R02', 'Bart Simpson', '0.5', 'S01'),
                 Reviewer('R03', 'Mickey Mouse', '0.4', 'S01'),
                 Reviewer('R04', 'Minie Mouse', '0.8', 'S02'),
                 Reviewer('R05', 'Oliver Quenn', '0.3', 'S02'),
                 Reviewer('R06', 'Clark Kent', '0.5', 'S03'),
                 Reviewer('R07', 'Bruce Wayne', '0.7', 'S03'),
                 Reviewer('R08', 'Louise Lane', '0.5', 'S04'),
                 Reviewer('R09', 'Lana Lang', '0.9', 'S04')]

    assignment = assign_review_random(submissions, reviewers, 5)

    return assignment


if __name__ == '__main__':
    app.run()


