import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions


def get_request(url, **kwargs):

    api_key = kwargs.get("api_key")

    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")
    if response:
        status_code = response.status_code
        json_data = json.loads(response.text)
        return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
  
    try:
            json_object = json.dumps(json_payload, indent = 4)
            print (json_object)
            response = requests.post(url, json_object,  headers={'Content-Type': 'application/json'})
            print('estoy aqui')
            print (response)
     
            if response:
                status_code = response.status_code
                print("With status {} ".format(status_code))
              

                return json_data
    except:
    # If any error occurs
        print("Network exception occurred")


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    dealer_id = kwargs.get("id")
    if dealer_id:
        json_result = get_request(url, id=dealer_id)
        if json_result:
            # Get the row list in JSON as dealers
            dealer = json_result
            # For each dealer object
            # Get its content in `doc` object
            dealer_doc = dealer[0]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                short_name=dealer_doc["short_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
            results = dealer_obj
    else:
        json_result = get_request(url)
        if json_result:
            # Get the row list in JSON as dealers
            dealers = json_result
            # For each dealer object
            for dealer in dealers:
                # Get its content in `doc` object
                dealer_doc = dealer["doc"]
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf ( url, dealer_id ):
    results = []
    json_result = get_request(url,  dealerId=dealer_id)
    if json_result:
        reviews = json_result['data']
    
        for review in reviews:
            review_doc = review
            review_obj = DealerReview(name = review_doc["name"], review=review_doc["review"],
                            dealership= review_doc["dealership"],
                            car_make=review_doc["car_make"], car_model=review_doc["car_model"], 
                            car_year = review_doc["car_year"],
                            purchase = review_doc["purchase"],
                            purchase_date = review_doc["purchase_date"][-4:], sentiment="") 
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    print (results)
    return results

# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
 
  api_key = "E-67hIJPjAJklz087WxyXcJqozOMNHm2u-5Oz6BDp074"
  url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/a7dde206-d4f7-4918-9d83-e0683d958ce1"
  authenticator = IAMAuthenticator(api_key)
  natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
    )


  natural_language_understanding.set_service_url(url)
  print (text)
  response = natural_language_understanding.analyze(
    text=text+"hello hello hello",
    features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()

  return response



# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative





