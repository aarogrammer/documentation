from datadog import initialize, api

options = {
    'api_key': '9775a026f1ca7d1c6c5af9d94d9595a4',
    'app_key': '87ce4a24b5553d2e482ea8a8500e71b8ad4554ff'
}

initialize(**options)

# Start a new discussion.
# Include a handle like this
api.Comment.create(
    handle='matt@example.com',
    message='Should we use COBOL or Fortran!'
)

# Or set it to None
# and the handle defaults
# to the owner of the application key
api.Comment.create(message='Should we use COBOL or Fortran?')

# Reply to a discussion.
api.Comment.create(
    handle='joe@example.com',
    message='Smalltalk?',
    related_event_id=1234
)
