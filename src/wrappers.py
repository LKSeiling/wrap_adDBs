import json
import time
import requests

class APICaller:

    def __init__(self):
        self.endpoint = None
        self.headers = None
        self.params = params
        self.token = None
        self.payload = None

    def get_request(self):
        try:
            response = requests.get(self.endpoint, headers=self.headers, data=json.dumps(self.payload), params=self.params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting {self.payload} from {self.endpoint}: {e}")

    def post_request(self):
        try:
            response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(self.payload), params=self.params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error posting {self.payload} to {self.endpoint}: {e}")

    def dictlist2csv(self, input_dictlist, path):
        df = pd.json_normalize(input_dictlist)
        df.to_csv(path, index=False)


class SnapWrapper(APICaller):
    
    def __init__(self):
        super().__init__()
        self.all_ads = []
        self.endpoint = "https://adsapi.snapchat.com/v1/ads_library/ads/search"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.payload = {
            "paying_advertiser_name": advertiser.lower()
            }
    
    def get_next_page(self, resp_json, query_url):
        get_ads = True
        res_url = ""
        try:
            new_url = resp_json.get('paging', {}).get('next_link')
            if new_url and new_url != query_url:
                res_url = new_url
            else:
                print("No new pagination link or duplicate link. Stopping.")
                get_ads = False
        except Exception as e:
            print(f"No new pagination link.")
            get_ads = False
        
        return res_url, get_ads
        
    def extract_ads(self, response):
        ads = []
        ids = []
        results = response.get("ad_previews", [])
        for ad_elem in results:
            ad = ad_elem['ad_preview']
            ad["matched_advertiser"] = advertiser
            ads.append(ad)
            ids.append(ad['id'])

    def query_by_advertiser_name(self, advertiser_name, retries = 5, sleep=10):
        get_ads = True
        counter = 0
        self.all_ads = []
        all_ids = []

        query_url = self.endpoint
        self.payload = {
            "paying_advertiser_name": advertiser_name.lower()
            }

        while get_ads:
            try:
                ads_before = len(set(all_ids))
            
                if query_url == self.endpoint: # inital call
                    response = self.post_request()
                else: # call based on response
                    self.payload["cursor"] = query_url.split("cursor=")[-1]
                    response = reqself.post_request()
            
                query_url, get_ads = get_next_page(response, query_url)
                
                ads, ids = extract_ads(response)
                self.all_ads = all_ads + ads
                all_ids = all_ids + ids

                if len(set(all_ids)) == ads_before:
                    print("🛑 No new ads added.")
                    counter = counter + 1
                    if counter >= retries:
                        get_ads = False

                time.sleep(sleep)

            except Exception as e:
                print(f"Error with advertiser {advertiser_name}: {e}")
        
        return all_ads