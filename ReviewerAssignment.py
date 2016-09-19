from flask import Flask
import random
import flask
import json

app = Flask(__name__)

# base class that will make all derivatives JSON serializable:
class JSONSerializable(list): # need to derive from a serializable class.

  def __init__(self, value = None):
    self = [ value ]

  def setJSONSerializableValue(self, value):
    self = [ value ]

  def getJSONSerializableValue(self):
    return self[1] if len(self) else None



class Submission(JSONSerializable):
    def __init__(self, submission_id, team_id):
        self.submission_id = submission_id
        self.team_id = team_id

    def __hash__(self):
        return hash((self.submission_id, self.team_id))

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class Reviwer(JSONSerializable):
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

                review_team.append(reviewers[reviewer_index])
                if reviewers[reviewer_index]['reviewer_id'] in reviewers_task_map.keys():
                    reviewers_task_map[reviewers[reviewer_index]['reviewer_id']].append(submissions[i])
                else:
                    this_reviewer_task = [submissions[i]]
                    reviewers_task_map[reviewers[reviewer_index]['reviewer_id']] = this_reviewer_task

            submission_reviewers_map[submissions[i]['submission_id']] = review_team
    else:
        raise ValueError('number of reviews per submission must be smaller than number of reviewers')


    return flask.jsonify(submissions=submission_reviewers_map, tasks=reviewers_task_map)

@app.route('/')
def hello_world():

    submissions = [{'submission_id':'S00', 'team_id':'T00'},
                   {'submission_id':'S01', 'team_id':'T01'},
                   {'submission_id':'S02', 'team_id':'T02'},
                   {'submission_id':'S03', 'team_id':'T03'},
                   {'submission_id':'S04', 'team_id':'T04'}]

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


