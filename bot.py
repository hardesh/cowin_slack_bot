#!/usr/bin/env python3

import sys
import requests
import json

import datetime

if __name__ == "__main__":
	# state_name = str(input("Enter the state name: "))
	# district_name = str(input("Enter the district name: "))
	# no_of_days = int(input("Enter the number of days to get appointments: "))
	
	state_name = "Maharashtra"
	district_name = "Pune"
	pincode_list = [411038, 411001, 411002, 411006, 411026, 411011] #411026, 411011
	no_of_days = 7

	start_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d-%m-%Y')

	date_list = []
	for i in range(no_of_days):
		date_list.append((datetime.datetime.today() + datetime.timedelta(days=i+1)).strftime('%d-%m-%Y'))
	# print(date_list)

	get_states = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states")
	states = get_states.json()
	
	state_id = -1
	for state_dict in states["states"]:
		if state_dict["state_name"] == state_name:
			state_id = state_dict["state_id"]
			break
	# print("state id: {}".format(state_id))

	if state_id == -1:
		print("Did not find state! Exiting! Check the spelling!")
		sys.exit()

	get_districts = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(state_id))
	districts = get_districts.json()

	district_id = -1
	for district_dict in districts["districts"]:
		if district_dict["district_name"] == district_name:
			district_id = district_dict["district_id"]
	# print("district_id is: {}".format(district_id))
	
	if district_id == -1:
		print("Did not find district! Exiting! Check the spelling!")
		sys.exit()

	# appointments = {_date: [] for _date in date_list}
	# for _date in date_list:
	# 	appoint_payload = {"district_id" : str(district_id), "date" : str(_date)}
	# 	get_appointments = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict", params=appoint_payload)
	# 	# appointments[_date].append(get_appointments.json()["sessions"])
	# 	appointments[_date] = get_appointments.json()["sessions"]
	# 	# print(get_appointments.json()["sessions"])

	# 	sessions = get_appointments.json()["sessions"]
	# 	for session in sessions:
	# 		# print(type(session["pincode"]))
	# 		if session["pincode"] in pincode_list:
	# 			# and session["min_age_limit"] <= 45
	# 			print(_date)
	# 			print(session)

	appoint_payload = {"district_id" : str(district_id), "date" : start_date}
	get_appointments = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict", params=appoint_payload)
	centers_list = get_appointments.json()["centers"]
	# print(get_appointments.json())
	available_centers = []
	for center in centers_list:
		# print(center)
		if center["sessions"][0]["min_age_limit"] < 45 and center["pincode"] in pincode_list:
			available_centers.append(center)
			# print(center)

	print(available_centers)
