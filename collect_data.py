from instagram.client import InstagramAPI
import os
import urllib

access_token = "1503846364.461e393.349bc641eed2421aad507296ea092956"
client_secret = "384018d7be63463a87ca48a9da21f17c"

#api = InstagramAPI(access_token=access_token, client_secret=client_secret)

def user(user_id):
	num_followed_by = 0
	num_follows = 0
	num_media = 0
	try:
		api = InstagramAPI(access_token=access_token, client_secret=client_secret)
		user = api.user(user_id)
		num_media = user.counts['media']
		num_followed_by = user.counts['followed_by']
		num_follows = user.counts['follows']
	except Exception as e:
		print(e)
	return num_followed_by,num_follows,num_media


def location_search(lat,lng):
	location_id_list = []
	try:
		api = InstagramAPI(access_token=access_token, client_secret=client_secret)
		locations = api.location_search(lat=lat,lng=lng,distance=5000)
		for location in locations:
			location_id_list.append(location.id)
	except Exception as e:
		print(e)
	return location_id_list


def location_recent_media(location_id):
	try:
		api = InstagramAPI(access_token=access_token, client_secret=client_secret)
		medias, next_ = api.location_recent_media(location_id=location_id,count=5000)
		for media in medias:
			if media.type == "image":
				media_id = media.id
				media_url = media.images['standard_resolution'].url
				user_id = media.user.id 
				location_id = media.location.id 
				location_name = media.location.name
				created_time = media.created_time

				tags = media.tags
				comments = media.comments
				caption = media.caption
				likes = len(media.likes)

				num_followed_by,num_follows,num_media = user(user_id)
				

				if not os.path.exists(media_id):
					os.makedirs(media_id)
				os.chdir(media_id)
				imagename = media_id + ".jpg"
				urllib.urlretrieve(media_url, imagename)
				filename = media_id + ".txt"
				f = open(filename, 'w')
				f.write("media_id" + "\t"  + media_id + "\n")
				f.write("user_id" + "\t" + user_id + "\n" )
				f.write("location_id" + "\t" + location_id + "\n" )
				f.write("location_name" + "\t" + str(location_name) + "\n" )
				f.write("created_time" + "\t" + str(created_time) + "\n" )
				f.write("caption" + "\t" + str(caption) + "\n")
				f.write("tags" + "\t")
				for tag in tags:
					f.write(str(tag) + "\t")
				f.write("\n")

				f.write("comments" + "\t")
				for comment in comments:
					f.write(str(comment) + "\t")
				f.write("\n")
				f.write("num_followed_by" + "\t" + str(num_followed_by) + "\n")
				f.write("num_follows" + "\t" + str(num_follows) + "\n")
				f.write("num_media" + "\t" + str(num_media) + "\n")
				f.close()
				os.chdir('..')
	except Exception as e:
		print(e)



def get_data(lat,lng,directory = "data"):
	#directory = "data"
	if not os.path.exists(directory):
		os.makedirs(directory)
	os.chdir(directory)

	location_id_list = location_search(lat,lng)
	print len(location_id_list)
	for location_id in location_id_list:
		location_recent_media(location_id)



if __name__ == '__main__':
	lat = "34.0500"
	lng = "118.2500"
	directory = "LA"
	get_data(lat,lng,directory)
	

    
    
