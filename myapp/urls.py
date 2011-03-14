# -*- coding: utf-8 -*-
# myapp.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('myapp/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'myapp/index': 'myapp.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='myapp.views.index'),
    Rule('/metabolic/global/<pathway_id>', endpoint='globalmetabolism', view='myapp.views.globalmetabolism'),
    Rule('/metabolic/pathway/<pathway_id>', endpoint='pathway', view='myapp.views.pathway')
  )
]

