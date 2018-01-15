from lxml import html  
import json
import requests
from time import sleep
import json,re

asin='B075QMZH2L'
boobs='small'
def ReviewCollector(page,asin):
    print(page)+'\n'
    #amazon_url  = 'http://www.amazon.com/dp/'+asin
    amazon_url= 'https://www.amazon.com/product-reviews/'+asin+'/ref=cm_cr_arp_d_show_all?ie=UTF8&reviewerType=all_reviews&pageNumber='+page
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(amazon_url,headers = headers)
    page_response = page.text
    parser = html.fromstring(page_response)
    XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
    XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'
    
    XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
    XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
    XPATH_PRODUCT_PRICE  = '//span[@id="priceblock_ourprice"]/text()'
    			
    raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
    product_price = ''.join(raw_product_price).replace(',','')
    raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
    product_name = ''.join(raw_product_name).strip()
    total_ratings  = parser.xpath(XPATH_AGGREGATE_RATING)
    reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
    if not reviews:
        reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
    ratings_dict = {}
    reviews_list = []
    			
    if not reviews:
        boobs='big'
    #grabing the rating  section in product page
    if boobs!='big':
        for ratings in total_ratings:
            extracted_rating = ratings.xpath('./td//a//text()')
            if extracted_rating:
                rating_key = extracted_rating[0] 
                raw_raing_value = extracted_rating[1]
                rating_value = raw_raing_value
                if rating_key:
                    ratings_dict.update({rating_key:rating_value})
        #Parsing individual reviews
        for review in reviews:
            XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
            XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
            XPATH_REVIEW_TEXT_1 = './/span[@data-hook="review-body"]//text()'
            XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
            XPATH_REVIEW_COMMENTS = './/span[@class="review-comment-total aok-hidden"]//text()'
            XPATH_AUTHOR  = './/a[contains(@href,"/profile/")]/parent::span//text()'
            XPATH_REVIEW_TEXT_3  = './/div[contains(@id,"dpReviews")]/div/text()'
            raw_review_author = review.xpath(XPATH_AUTHOR)
            raw_review_rating = review.xpath(XPATH_RATING)
            raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
            raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
            raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
            raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)
            author = ' '.join(' '.join(raw_review_author).split()).strip('By')
            review_rating = ''.join(raw_review_rating).replace('out of 5 stars','')
            review_header = ' '.join(' '.join(raw_review_header).split())
            review_text = ' '.join(' '.join(raw_review_text1).split())
            
        
            raw_review_comments = review.xpath(XPATH_REVIEW_COMMENTS)
            review_comments = ''.join(raw_review_comments)
            review_comments = re.sub('[A-Za-z]','',review_comments).strip()
            review_dict = {
        									'review_comment_count':review_comments,
        									'review_text':review_text,'review_header':review_header,
        									'review_rating':review_rating,
        									'review_author':author
                                            }
        								
        								
        								
            reviews_list.append(review_dict)
            #print(review_dict)
    
    
    data = {
    						'ratings':ratings_dict,
    						'reviews':reviews_list,
    						'url':amazon_url,
    						'price':product_price,
    						'name':product_name
    					}
    return(data)  
    
    
    
    
def ReadAsin():
    ProductsAsin=['B075QMZH2L','B0785H6VKX','B076HQ6FSY','B01MUSD2ST']
    for asin in ProductsAsin:
        extracted_data=[]
        page=1
        filename=asin+'.json'
        while(page<7):
            extracted_data.append(ReviewCollector(str(page),asin))
            f=open(filename,'w')
            json.dump(extracted_data,f,indent=4)
            page=page+1;
            sleep(5)

if __name__ == '__main__':
    ReadAsin()