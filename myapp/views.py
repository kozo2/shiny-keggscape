# -*- coding: utf-8 -*-
"""
myapp.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""

from kay.utils import render_to_response

from google.appengine.api import urlfetch
import re
from operator import itemgetter

from werkzeug import Response

# Create your views here.

class Organism:
  def __init__(self, code, name):
    self.code = code
    self.name = name

def index(request):
  return render_to_response('myapp/index.html', {'message': 'Hello'})

def globalmetabolism(request, pathway_id):
  result = urlfetch.fetch("http://www.kegg.com/kegg/pathway/map/map" + pathway_id + ".html")
  pathway_re = re.compile(r'KEGG PATHWAY:.+') 
  pathway_name = pathway_re.findall(result.content)[0].split(": ")[1].replace(" - Reference pathway", "")

  org_re = re.compile(r'<option\s{1}value="\w{3}">.+')
  organisms = []
  organism_name_for = {}
  orgs = org_re.findall(result.content)

  for org in orgs:
      org_code = org.split('"')[1]
      org_name = org.split('>')[1]
      #organisms.append(Organism(org_code, org_name))
      organism_name_for[org_code] = org_name

  # sort by organism name
  alphabetical_organism = sorted(organism_name_for.iteritems(), key = itemgetter(1))

  if request.method == "POST":
    json_layout = urlfetch.fetch("http://dl.dropbox.com/u/157897/bsu01100layout.json").content
    json_data   = urlfetch.fetch("http://dl.dropbox.com/u/157897/bsu01100data.json").content
    selected_organism_code = request.form['organism']
    selected_organism_name = organism_name_for[selected_organism_code]
    return render_to_response('myapp/globalmetabolism_cy.html', {'pathway_id': pathway_id, 'pathway_name': pathway_name, 'alphabetical_organism': alphabetical_organism, 'selected_organism_code': selected_organism_code, 'selected_organism_name': selected_organism_name, 'json_layout': json_layout, 'json_data': json_data})

  else:
    return render_to_response('myapp/globalmetabolism.html', {'pathway_id': pathway_id, 'pathway_name': pathway_name, 'alphabetical_organism': alphabetical_organism})

def pathway(request, pathway_id):
  result = urlfetch.fetch("http://www.kegg.com/kegg/pathway/map/map" + pathway_id + ".html")
  pathway_re = re.compile(r'KEGG PATHWAY:.+') 
  pathway_name = pathway_re.findall(result.content)[0].split(": ")[1].replace(" - Reference pathway", "")

  org_re = re.compile(r'<option\s{1}value="\w{3}">.+')
  organisms = []
  organism_name_for = {}
  orgs = org_re.findall(result.content)

  for org in orgs:
      org_code = org.split('"')[1]
      org_name = org.split('>')[1]
      organisms.append(Organism(org_code, org_name))
      organism_name_for[org_code] = org_name

  # sort by organism name
  alphabetical_organism = sorted(organism_name_for.iteritems(), key = itemgetter(1))

  if request.method == "POST":
    selected_organism_code = request.form['organism']
    selected_organism_name = organism_name_for[selected_organism_code]

    json_layout = urlfetch.fetch("http://cg06.naist.jp/metadav/layout/" + selected_organism_code + pathway_id + "layout.json").content
    json_data   = urlfetch.fetch("http://cg06.naist.jp/metadav/data/" + selected_organism_code + pathway_id + "data.json").content

    #json_layout = urlfetch.fetch("http://dl.dropbox.com/u/157897/bsu00020layout.json").content
    #json_data   = urlfetch.fetch("http://dl.dropbox.com/u/157897/bsu00020data.json").content

    return render_to_response('myapp/cytoscape.html', {'pathway_id': pathway_id, 'pathway_name': pathway_name, 'alphabetical_organism': alphabetical_organism, 'selected_organism_code': selected_organism_code, 'selected_organism_name': selected_organism_name, 'json_layout': json_layout, 'json_data': json_data})

  else:
    return render_to_response('myapp/pathway.html', {'pathway_id': pathway_id, 'pathway_name': pathway_name, 'alphabetical_organism': alphabetical_organism})
