import requests
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urljoin, urlparse
import re
import json
import random
import string

def analysis(url, user_agent):

    results = []

    #declare globally lists to avoid crawling website url multiple times
    global crawled_urls
    global urls_to_crawl
    crawled_urls = []
    urls_to_crawl = []

    urls_to_crawl.append(url)

    #until there are urls to "crawl"
    while True:

        #if there are no urls, break while loop
        if not urls_to_crawl:
            break

        for url in urls_to_crawl:

            #check if url is checked or not
            checkedUrl = checkIfInCrawled(url)

            if checkedUrl == True:
                urls_to_crawl.remove(url)
                continue
            else:
                #if url to crawl is not in crawled_urls, call website analysis
                urlAnalysis = website_analysis(url, user_agent)
                crawled_urls.append(url)
                results.append(urlAnalysis)
                continue

    return results

def checkIfInCrawled(url):

    #if url to crawl is in crawled_urls, remove crawled url
    for curl in crawled_urls:
        if url == curl:
            return True
        else:
            continue
    else:
        return False

def checkIfInQueryToCrawl(url):

    #check if url is in the query to crawl
    for curl in urls_to_crawl:
        if url == curl:
            return True
        else:
            continue
    else:
        return False

def website_analysis(url, user_agent):

    #declare headers
    headers = {
        "User-agent": user_agent
    }

    #create request
    soup = make_soup(url, headers)

    #get basic info
    url_status = check_status(url)
    ssl = check_ssl(url)
    meta_robots_info = get_meta_robots_info(soup)
    response_time = get_response_time(url, headers)
    titles = get_title_tag(soup)
    descriptions = get_meta_descriptions(soup)
    h1 = get_h1(soup)
    h2 = get_h2(soup)
    other_h = get_other_h(soup)
    url_title = get_url_title(url)

    #get keyword based on data above
    keyword = get_keyword(
        titles[0] if titles else None,
        descriptions[0] if descriptions else None,
        h1[0] if h1 else None,
        url_title)

    #get main title based on keyword and len of title
    main_title = get_main_title(keyword, titles)

    #get main h1 based on keyword and len of h1
    main_h1 = get_main_h1(keyword, h1)

    #get main description based on keyword and len of descriptions
    main_description = get_main_description(keyword, descriptions)

    #internal and external links
    urls_info = get_internal_and_external_links(url, soup)
    external_links = urls_info['external_links']
    internal_links = urls_info['internal_links']

    #append internal links to urls_to_crawl
    #but first, check if internal url is in crawled_urls
    for interurl in internal_links:

        #but first, check if internal url is in crawled_urls
        checkedUrl = checkIfInCrawled(interurl)
        if checkedUrl == True:
            continue

        #check if internal url is already in query to crawl
        inQueryUrl = checkIfInQueryToCrawl(interurl)
        if inQueryUrl == True:
            continue

        #add to urls to crawl
        urls_to_crawl.append(interurl)

    #images and keyword extraction
    images = get_images(url, soup)
    images_links = get_links_images(url, soup, images)

    #analyze data
    responseTimeAnalysis = response_time_analysis(response_time)
    titleAnalysis = title_list_analysis(keyword, titles)
    h1_analysis = h1_list_analysis(keyword, h1)
    h2_analysis = h2_list_analysis(h2)
    other_h_analysis = other_h_list_analysis(other_h)
    descriptions_analysis = descriptions_list_analysis(keyword, descriptions)
    urlTitleAnalysis = url_title_analysis(keyword, url_title)
    #external_links_status = get_links_status(external_links)
    #internal_links_status = get_links_status(internal_links)
    externalLinksAnalysis = external_links_analysis(external_links)
    internalLinksAnalysis = internal_links_analysis(internal_links)
    images_analysis = get_images_analysis(url, soup)

    #Append all stuff to competitions
    results = {
        'url' : url,
        'url_status': url_status,
        'ssl': {
            'analysis': ssl
        },
        'meta_robots': meta_robots_info,
        'response_time': {
            'time': response_time * 1000,
            'analysis': responseTimeAnalysis
        },
        'keyword': keyword,
        'title' : {
            'title_count': len(titles),
            'main_title': main_title,
            'titles': titles,
            'analysis': titleAnalysis
        },
        'description': {
            'descriptions_count': len(descriptions),
            'main_description': main_description,
            'descriptions': descriptions,
            'analysis': descriptions_analysis
        },
        'url_title': {
            'url_title': url_title,
            'analysis': urlTitleAnalysis
        },
        'h1': {
            'h1_count': len(h1),
            'main_h1': main_h1,
            'h1': h1,
            'analysis': h1_analysis
        },
        'h2': {
            'h2_count': len(h2),
            'h2': h2,
            'analysis': h2_analysis
        },
        'other_h': {
            'other_h_count': len(other_h),
            'other_h': other_h,
            'analysis': other_h_analysis
        },
        'external_links': {
            'external_links_count': len(external_links),
            'external_links': external_links,
            #'status': external_links_status,
            'analysis': externalLinksAnalysis
        },
        'internal_links': {
            'internal_links_count': len(internal_links),
            'internal_links': internal_links,
            #'status': internal_links_status,
            'analysis': internalLinksAnalysis
        },
        'images': {
            'images_counts': len(images),
            'images': images_links,
            'analysis': images_analysis
        }
    }

    return results

def make_soup(url, headers):
    r = requests.get(url, headers = headers, verify = False).content
    soup = BeautifulSoup(r, 'html.parser', from_encoding='utf-8')
    return soup

def get_response_time(url, headers):
    r = requests.get(url, headers = headers)
    response_time = r.elapsed.total_seconds()
    return response_time

def response_time_analysis(response_time):

    #convert seconds to milliseconds
    response_time = response_time * 1000

    #round to two decimal places
    response_time = round(response_time, 2)

    if response_time <= 0.00:
        return [{
            "status": "Invalid",
            "message": "The response time of the website is too low and amounts to: {:.2f} miliseconds.".format(response_time)
        }]
    if 0.00 < response_time <= 200.00:
        return [{
            "status": "Valid",
            "message": "The page response time is low and amounts to: {:.2f} miliseconds.".format(response_time)
        }]
    elif response_time > 200.00:
        return [{
            "status": "Invalid",
            "message": "Page response time is too high and is: {:.2f} miliseconds.".format(response_time)
        }]

def check_robots_txt(url, headers):

    base_url = get_base_url(url)

    #check robots.txt
    result = os.popen("curl " + base_url + "robots.txt").read()
    result_data_set = {"Disallowed":[], "Allowed":[]}

    for line in result.split("\n"):
        if line.startswith('Allow'):    # this is for allowed url
            result_data_set["Allowed"].append(base_url + line.split(': ')[1].split(' ')[0])
        elif line.startswith('Disallow'):    # this is for disallowed url
            result_data_set["Disallowed"].append(base_url + line.split(': ')[1].split(' ')[0])

    if result_data_set["Allowed"]:
        return result_data_set["Allowed"]
    else:
        return False

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_meta_robots_info(soup):

    meta_robots = soup.find("meta",  content = "noindex")

    if meta_robots:
        return [{
            "status": "Invalid",
            "message": "The page has a meta({}) attribute with specified non-indexing it in search engines.".format(meta)
        }]
    else:
        return [{
            "status": "Valid",
            "message": "The page does not have a meta attribute that blocks indexing of the page."
        }]

def get_h1(soup):

    h1 = soup.find_all('h1')
    results = []

    if h1:
        temp_result = (h.text for h in h1)
        for h in temp_result:
            h = h.replace('\r\n', '').replace('\n', '').replace('\r', '').replace('  ', '').replace('   ', '').replace('    ', '').replace('. ','.').replace('\xa0', ' ')
            results.append(h)
    else:
        pass

    return results

def get_h2(soup):

    h2 = soup.find_all('h2')
    results = []

    if h2:
        temp_result = (h.text for h in h2)
        for h in temp_result:
            h = h.replace('\r\n', '').replace('\n', '').replace('\r', '').replace('  ', '').replace('   ', '').replace('    ', '').replace('. ','.').replace('\xa0', ' ')
            results.append(h)
    else:
        pass

    return results

def get_other_h(soup):

    h_others = soup.find_all(re.compile('^h[3-6]$'))
    results = []

    if h_others:
        temp_result = (h.text for h in h_others)
        for h in temp_result:
            h = h.replace('\r\n', '').replace('\n', '').replace('\r', '').replace('  ', '').replace('   ', '').replace('    ', '').replace('. ','.').replace('\xa0', ' ')
            results.append(h)
    else:
        pass

    return results

def get_title_tag(soup):

    results = []

    for title in soup.findAll("title"):
        if title:
            title_text = (title.text).replace('\r\n', '').replace('\n', '').replace('\r', '').replace('  ', '').replace('   ', '').replace('    ', '').replace('. ','.').replace('\xa0', ' ')
            results.append(str(title_text))
        else:
            pass

    if not results:
        pass

    return results

def get_meta_descriptions(soup):

    results = []

    for meta in soup.findAll("meta"):
        if meta:
            metaname = meta.get('name', '').lower()
            metaprop = meta.get('property', '').lower()
            if 'description' == metaname or metaprop.find("description")>0:
                desc = meta['content'].strip()
                results.append(desc)
        else:
            pass

    if not results:
        pass

    return results

def get_images(url, soup):

    images = soup.find_all('img')

    return images

def get_links_images(url, soup, images):

    results = []
    base_url = get_base_url(url)

    for image in images:
        image_url = base_url + image.get('src')
        results.append(image_url)

    return results

def get_images_analysis(url, soup):

    results = []

    base_url = get_base_url(url)
    images = soup.find_all('img')
    reqs = (requests.get(base_url + pic.get('src')) for pic in images)

    #open every image in new window and check attributes and size
    for r in reqs:
        path, file_ = os.path.split('{}'.format(soup.find('img').get('src')))
        image_size = round(len(r.content)/(1024))
        image_alt = soup.find('img').get('alt')

        if image_size < 200:
            results.append({
                "url": r.url,
                "file_name": file_,
                "status": "Valid",
                "message": "The photo size is correct and is {}.".format(image_size)
            })

        if image_size >= 200:
            results.append({
                "url": r.url,
                "file_name": file_,
                "status": "Invalid",
                "message": "The photo size is too large. Current: {}. Suggested: 200MB.".format(image_size)
            })

        if not image_alt:
            results.append({
                "url": r.url,
                "file_name": file_,
                "status": "Invalid",
                "message": "The photo has no alt attribute."
            })

        if image_alt is None:
            results.append({
                "url": r.url,
                "file_name": file_,
                "status": "Invalid",
                "message": "The photo has an empty alt attribute."
            })

        if image_alt:
            results.append({
                "url": r.url,
                "file_name": file_,
                "status": "Valid",
                "message": "The photo has a valid alt attribute({}).".format(image_alt)
            })

            #check alt attribute length
            if 115 < len(image_alt) < 135:
                results.append({
                    "url": r.url,
                    "file_name": file_,
                    "status": "Valid",
                    "message": "The alt({}) attribute of the photo is the correct length.".format(image_alt)
                })

            elif len(image_alt) <= 115:
                free_characters = 115 - len(image_alt)
                results.append({
                    "url": r.url,
                    "file_name": file_,
                    "status": "Valid",
                    "message": "The alt({}) attribute of the photo is too short. Add at least {} characters to it.".format(image_alt, free_characters)
                })

            elif len(image_alt) > 135:
                free_characters = len(image_alt) - 135
                results.append({
                    "url": r.url,
                    "file_name": file_,
                    "status": "Valid",
                    "message": "The alt({}) attribute of the photo is too long. Shorten it by at least {} characters.".format(image_alt, free_characters)
                })

    return results

def get_base_url(url):

    url_splited = urlsplit(url)
    base_url = url_splited.scheme + "://" + url_splited.netloc + "/"

    return base_url

def get_internal_and_external_links(url, soup):

    internal_links = []
    external_links = []

    base_url = get_base_url(url)

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_links:
            # already in the set
            continue
        if 'javascript://void(0)' in href:
            #remove all void hrefs
            continue
        if 'mailto://' in href:
            #and mail hrefs
            continue
        if 'call://' in href:
            #and call hrefs
            continue
        if 'tel:' in href:
            #and call hrefs
            continue
        if base_url not in href:
            # check if url is not in external link
            if href not in external_links:
                external_links.append(href)
            continue

        internal_links.append(href)

    context = {
        'external_links' : external_links,
        'internal_links' : internal_links,
    }

    return context

def get_url_title(url):

    title = urlparse(url).path

    if str(title) == "/":
        return None

    return title

def get_keyword(title, meta_desc, h1, url_title):

    #if one of parameters is None, match to it random hash
    if title is not None:
        title = title.lower()
    else:
        title = get_random_string(8)
    if meta_desc is not None:
        meta_desc = meta_desc.lower()
    else:
        meta_desc = get_random_string(8)
    if h1 is not None:
        h1 = h1.lower()
    else:
        h1 = get_random_string(8)
    if url_title is not None:
        url_title = url_title.lower()
    else:
        url_title = get_random_string(8)

    #hierarchy of elements:
    #   1 url_title
    #   2 title
    #   3 meta_desc
    #   4 h1_list

    #some of combinations of keyword extraction
    if url_title in title:
        if url_title in meta_desc:
            return url_title

    if url_title in title:
        if title in meta_desc:
            return title

    if url_title in title:
        if url_title in h1:
            return url_title

    if url_title in title:
        if h1 in url_title:
            return h1

    if url_title in meta_desc:
        if url_title in h1:
            return url_title

    if url_title in meta_desc:
        if h1 in url_title:
            return h1

    if title in meta_desc:
        if title in h1:
            return title

    if title in meta_desc:
        if h1 in title:
            return h1

    if h1 in url_title:
        if h1 in title:
            return h1

    if h1 in url_title:
        if h1 in meta_desc:
            return h1

    if h1 in title:
        if h1 in meta_desc:
            return h1

    if title:
        return title

    if meta_desc:
        return meta_desc

    if h1:
        return h1

    return None

def get_random_string(length):
    # put your letters in the following string
    sample_letters = 'abcdefghijklmnopqrstuvwxyz'
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))

    return result_str

def check_status(url):

    r = requests.get(url)
    status = r.status_code

    return status

def check_ssl(url):

    if "https" in str(url):
        return [{
            "status": "Valid",
            "message": "The website has an ssl certificate."
        }]
    else:
        return [{
            "status": "Invalid",
            "message": "The website does not have an ssl certificate."
        }]

def get_links_status(urls):

    results = []

    for url in urls:
        status = check_status(url)

        if status == 200:
            results.append({
                "url": url,
                "url_status": status,
                "status": "Valid",
                "message": "Correct status."
            })
        else:
            results.append({
                "url": url,
                "url_status": status,
                "status": "Invalid",
                "message": "The page status is incorrect."
            })

    return results

def get_main_h1(keyword, h1):

    if len(h1) == 1:
        return h1[0]
    elif len(h1) < 1:
        return None
    else:
        #clean h1 to get h1 with keyword inside only
        h1_with_keyword = []
        for tag in h1:
            if keyword.lower() in tag.lower():
                h1_with_keyword.append(tag)
            else:
                continue

        #return the shortest h1, null or the only h1
        if len(h1_with_keyword) > 1:

            #we assume, that if there are two the same titles, min_desc is None
            min_desc = min(h1_with_keyword, key = len)

            if min_desc:
                return min_desc
            else:
                return h1_with_keyword[0]

        # if there is 1 title, return him or get first from h1 list
        elif len(h1_with_keyword) == 1:
            return h1_with_keyword[0]

        #remove duplicates if exists, and return first element
        elif len(set(h1)) == 1:
            return h1[0]

    return None

def get_main_title(keyword, titles):

    if len(titles) == 1:
        return titles[0]
    elif len(titles) < 1:
        return None
    else:
        #clean h1 to get title with keyword inside only
        titles_with_keyword = []
        for tag in titles:
            if keyword.lower() in tag.lower():
                titles_with_keyword.append(tag)
            else:
                continue

        #return the shortest title, null or the only title
        if len(titles_with_keyword) > 1:

            #we assume, that if there are two the same titles, min_desc is None
            min_desc = min(titles_with_keyword, key = len)

            if min_desc:
                return min_desc
            else:
                return titles_with_keyword[0]

        # if there is 1 title, return him or get first from h1 list
        elif len(titles_with_keyword) == 1:
            return titles_with_keyword[0]

        #remove duplicates if exists, and return first element
        elif len(set(titles)) == 1:
            return titles[0]

    return None

def get_main_description(keyword, descriptions):

    if len(descriptions) == 1:
        return descriptions[0]
    elif len(descriptions) < 1:
        return None
    else:
        #clean descriptions to get descriptions with keyword inside only
        descriptions_with_keyword = []
        for tag in descriptions:
            if keyword.lower() in tag.lower():
                descriptions_with_keyword.append(tag)
            else:
                continue

        #return the shortest descriptions, null or the only descriptions
        if len(descriptions_with_keyword) > 1:

            #we assume, that if there are two the same descriptions, min_desc is None
            min_desc = min(descriptions_with_keyword, key = len)

            if min_desc:
                return min_desc
            else:
                return descriptions_with_keyword[0]

        # if there is 1 title, return him or get first from h1 list
        elif len(descriptions_with_keyword) == 1:
            return descriptions_with_keyword[0]

        #remove duplicates if exists, and return first element
        elif len(set(descriptions)) == 1:
            return descriptions[0]

    return None

def descriptions_list_analysis(keyword, descriptions):

    if len(descriptions) < 1:

        return [{
            "status": "Invalid",
            "message": "There is no description tag on the page."
        }]

    elif len(descriptions) == 1:

        results = [{
            "status": "Valid",
            "message": "Description tag found on page."
        }]

        analysis = description_analysis(keyword, descriptions[0])
        results.extend(analysis)

        return results

    elif len(descriptions) > 1:

        results = [{
            "status": "Invalid",
            "message": "The size of description tag on the page is too large."
        }]

        for tag in descriptions:
            analysis = description_analysis(keyword, tag)
            results.extend(analysis)

        return results

def description_analysis(keyword, description):

    results = []

    if keyword is None:
        keyword = get_random_string(8)

    #check if keyword exists in description tag
    if keyword.lower() in description.lower():
        results.append({
            "status": "Valid",
            "message": "The description({}) tag contains a key word or phrase.".format(description)
        })
    else:
        results.append({
            "status": "Invalid",
            "message": "The description({}) tag does not contain a keyword or phrase.".format(description)
        })

    #check length of description
    if len(description) >= 50 <= 160:
        results.append({
            "status": "Valid",
            "message": "The description({}) tag is the correct length.".format(description)
        })
    elif len(description) < 50:
        free_characters = 50 - len(description)
        results.append({
            "status": "Invalid",
            "message": "The description({}) tag is too short. Add {} characters to it.".format(description, free_characters)
        })
    else:
        free_characters = len(description) - 160
        results.append({
            "status": "Invalid",
            "message": "The description({}) tag is too long. Shorten it by {} characters.".format(description, free_characters)
        })

    return results

def title_list_analysis(keyword, titles):

    if len(titles) < 1:

        return [{
            "status": "Invalid",
            "message": "There is no title tag on the page."
        }]

    elif len(titles) == 1:

        results = [{
            "status": "Valid",
            "message": "Title tag found on the page."
        }]

        analysis = title_analysis(keyword, titles[0])
        results.extend(analysis)

        return results

    elif len(titles) > 1:

        results = [{
            "status": "Invalid",
            "message": "The amount of title tag on the page is too large."
        }]

        for tag in titles:
            analysis = title_analysis(keyword, tag)
            results.extend(analysis)

        return results

def title_analysis(keyword, title):

    results = []

    #if keyword is None, match to it random string
    if keyword is None:
        keyword = get_random_string(8)

    #check length of title
    if len(title) >= 50 <= 60:
        results.append({
            "status": "Valid",
            "message": "The title({}) tag is the correct length.".format(title)
        })
    elif len(title) < 50:
        free_characters = 50 - len(title)
        results.append({
            "status": "Invalid",
            "message": "The title({}) tag is too short. Add {} characters to it.".format(title, free_characters)
        })
    else:
        free_characters = len(title)- 60
        results.append({
            "status": "Invalid",
            "message": "The title({}) tag is too long. Shorten it by {} characters.".format(title, free_characters)
        })

    return results

def url_title_analysis(keyword, url_title):

    results = []

    #if keyword is None, match to it random string
    if keyword is None:
        keyword = get_random_string(8)

    #if url_title is None, match to it random string
    if url_title is None:
        return None

    #check if keyword exists in url_title
    if keyword.lower() in url_title.lower().replace('-', ' ').replace('_', ' '):
        results.append({
            "status": "Valid",
            "message": "Url title({}) contains a keyword or phrase.".format(url_title)
        })
    else:
        results.append({
            "status": "Invalid",
            "message": "Url title({}) does not contain a keyword or phrase.".format(url_title)
        })

    return results

def h1_list_analysis(keyword, h1):

    if len(h1) < 1:

        return [{
            "status": "Invalid",
            "message": "There is no h1 tag on the page."
        }]

    elif len(h1) == 1:

        results = [{
            "status": "Valid",
            "message": "H1 tag found on the page."
        }]

        analysis = h1_analysis(keyword, h1[0])
        results.extend(analysis)

        return results

    elif len(h1) > 1:

        results = [{
            "status": "Invalid",
            "message": "The amount of h1 tag on the page is too large."
        }]

        for tag in h1:
            analysis = h1_analysis(keyword, tag)
            results.extend(analysis)

        return results

def h1_analysis(keyword, h1):

    results = []

    #if keyword is None, match to it random string
    if keyword is None:
        keyword = get_random_string(8)

    #check if keyword exists in h1 tag
    if keyword.lower() in h1.lower():
        results.append({
            "status": "Valid",
            "message": "The h1({}) tag contains a key word or phrase.".format(h1)
        })
    else:
        results.append({
            "status": "Invalid",
            "message": "The h1({}) tag does not contain a keyword or phrase.".format(h1)
        })

    #check length of h1
    if len(h1) >= 20 <= 70:
        results.append({
            "status": "Valid",
            "message": "The h1({}) tag is the correct length.".format(h1)
        })
    elif len(h1) < 20:
        free_characters = 20 - len(h1)
        results.append({
            "status": "Invalid",
            "message": "The h1({}) tag is too short. Add {} characters to it.".format(h1, free_characters)
        })
    else:
        free_characters = len(h1)- 70
        results.append({
            "status": "Invalid",
            "message": "The h1({}) tag is too long. Shorten it by {} characters.".format(h1, free_characters)
        })

    return results

def h2_list_analysis(h2):

    if len(h2) < 1:

        return [{
            "status": "Invalid",
            "message": "There are no h2 tags on the page."
        }]

    elif len(h2) == 1:

        free_h2_tags = 4 - len(h2)

        results = [{
            "status": "Invalid",
            "message": "Too few h2 tags on the page. Add at least {} tags.".format(free_h2_tags)
        }]

        analysis = h2_analysis(h2[0])
        results.extend(analysis)

        return results

    elif len(h2) >= 2:

        results = [{
            "status": "Valid",
            "message": "The correct number of h2 tags on the page."
        }]

        for tag in h2:
            analysis = h2_analysis(tag)
            results.extend(analysis)

        return results

def h2_analysis(h2):

    results = []

    #check length of h1
    if 20 <= len(h2) <= 70:
        results.append({
            "status": "Valid",
            "message": "The h2({}) tag is the correct length.".format(h2)
        })
    elif len(h2) < 20:
        free_characters = 20 - len(h2)
        results.append({
            "status": "Invalid",
            "message": "The h2({}) tag is too short. Add {} characters to it.".format(h2, free_characters)
        })
    else:
        free_characters = len(h2)- 70
        results.append({
            "status": "Invalid",
            "message": "The h2({}) tag is too long. Shorten it by {} characters.".format(h2, free_characters)
        })

    return results

def other_h_list_analysis(other_h):

    if len(other_h) is None:

        return [{
            "status": "Invalid",
            "message": "There are no h3-h6 tags on the page."
        }]

    elif len(other_h) < 4:

        free_other_h_tags = 4 - len(other_h)

        return [{
            "status": "Invalid",
            "message": "Too few h3-h6 tags on the page. Add at least {} tags.".format(free_other_h_tags)
        }]

    elif len(other_h) >= 4:

        return [{
            "status": "Valid",
            "message": "The correct number of h3-h6 tags on the page."
        }]

def external_links_analysis(external_links):

    if len(external_links) is None:

        return [{
            "status": "Invalid",
            "message": "No external links on the site."
        }]

    elif len(external_links) < 3:

        free_external_links = 3 - len(external_links)

        results = [{
            "status": "Invalid",
            "message": "Too few external links on the page. Add at least {} links.".format(free_external_links)
        }]

        return results

    elif len(external_links) >= 3:

        results = [{
            "status": "Valid",
            "message": "Correct number of external links on the page."
        }]

        return results

def internal_links_analysis(internal_links):

    if len(internal_links) is None:

        return [{
            "status": "Invalid",
            "message": "No internal links on the page."
        }]

    elif len(internal_links) < 10:

        free_internal_links = 10 - len(internal_links)

        results = [{
            "status": "Invalid",
            "message": "Too few internal links on the page. Add at least {} links.".format(free_internal_links)
        }]

        return results

    elif len(internal_links) >= 10:

        results = [{
            "status": "Valid",
            "message": "The correct number of internal links on the page."
        }]

        return results
