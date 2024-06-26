import os
from tournaments import fetch_tournaments
from standings import mainWorker
from supabase_client import supabase_client
import json
import time

# mainWorker("0000090", "BA189xznzDvlCdfoQlBC", False, False)

# for tournament in data:
#   #if (tournament['tournamentStatus'] != 'finished'):
#   print('Updating tournament - ' + tournament['name'])
#   mainWorker(tournament, False, False, data)

def load_all_past_tournaments():
  print('Fetching past tournaments...')
  # tournaments = fetch_tournaments(should_fetch_past_events=True)
  f = open('smol-tournaments.json', encoding="utf8")
  tournaments = json.load(f)


  formats = supabase_client.table('Formats').select('id,format,rotation,start_date').execute().data
  for tournament in tournaments:
    print('Updating tournament - ' + tournament['name'])
    mainWorker(tournament, True, False, tournaments, formats, False, False)

  print('Done!')

def load_past_tournament(tournament_id):
  print('Loading tournament with id', tournament_id)

  tournament = supabase_client.table('tournaments_new').select('*').eq('id', tournament_id).execute().data[0]
  formats = supabase_client.table('Formats').select('id,format,rotation,start_date').execute().data

  print('Updating tournament - ' + tournament['name'])
  mainWorker(tournament, True, False, [tournament], formats, False, False)

  print('Done!')

def load_tournament_json(tournament_json):
  formats = supabase_client.table('Formats').select('id,format,rotation,start_date').execute().data

  print('Updating tournament - ' + tournament_json['name'])
  mainWorker(tournament_json, True, False, [tournament_json], formats, False, False)

  print('Done!')


def update_live_and_upcoming_tournaments():
  print('Fetching live and upcoming tournaments...')

  tournaments = fetch_tournaments(False, False)
  formats = supabase_client.table('Formats').select('id,format,rotation,start_date').execute().data

  for tournament in tournaments:
    print('Updating tournament - ' + tournament['name'])
    mainWorker(tournament, False, False, tournaments, formats, True, False)

  print('Done!')

def delete_past_tournament(tournament_id):
  print('Deleting tournament with id', tournament_id)

  supabase_client.table('tournaments_new').delete().eq('id', tournament_id).execute()

  print('Done!')

# VGC!
def update_live_and_upcoming_vgc_tournaments():
  print('VGC == Fetching live and upcoming tournaments...')

  tournaments = fetch_tournaments(False, True)

  for tournament in tournaments:
    print('Updating VGC tournament - ' + tournament['name'])
    mainWorker(tournament, False, False, tournaments, [], True, True)

  print('Done!')

# VGC!
def load_all_past_vgc():
  print('VGC == Fetching past tournaments...')

  tournaments = fetch_tournaments(True, True)

  for tournament in tournaments:
    print('Updating VGC tournament - ' + tournament['name'])
    mainWorker(tournament, False, False, tournaments, [], False, True)

  print('Done!')

# load_all_past_tournaments()
# delete_past_tournament(58)
while True:
  update_live_and_upcoming_tournaments()
  update_live_and_upcoming_vgc_tournaments()
  print('...zzz...')
  time.sleep(60)