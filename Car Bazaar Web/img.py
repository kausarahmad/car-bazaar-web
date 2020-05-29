from google_images_search import GoogleImagesSearch

# if you don't enter api key and cx, the package will try to search
# them from environment variables GCS_DEVELOPER_KEY and GCS_CX
gis = GoogleImagesSearch('AIzaSyBfe3QCglu_T0ldNUFoeUVY8LJ6XexbajQ', '016040578520524185149:aj1ixvinhes')

# example: GoogleImagesSearch('ABcDeFGhiJKLmnopqweRty5asdfghGfdSaS4abC', '012345678987654321012:abcde_fghij')

# define search params:
_search_params = {
    'q': 'Toyota Corolla Gli 2000',
    'num': 10,
    'fileType': 'jpg'
}

""" # this will only search for images:
gis.search(search_params=_search_params)

# this will search and download:
gis.search(search_params=_search_params, path_to_dir='/path/')

# this will search, download and resize:
gis.search(search_params=_search_params, path_to_dir='/path/', width=500, height=500) """

# search first, then download and resize afterwards:
gis.search(search_params=_search_params)
for image in gis.results():
    image.download("C:\\Users\\kausa\\Desktop\\Car Bazaar Web\\Car Bazaar Web\\static\\img\\chat page car\\")