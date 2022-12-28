from re import finditer, escape

def analize_content(keyword, text, page_title, meta_description):

    textAnalysis = text_analysis(text, keyword)
    keywordAnalysis = keyword_analysis(keyword)
    titleAnalysis = title_analysis(keyword, page_title)
    metaDescriptionAnalysis = meta_description_analysis(keyword, meta_description)

    results = {
        'keyword': {
            'keyword': keyword,
            'analysis': keywordAnalysis
        },
        'page_title': {
            'page_title': page_title,
            'analysis': titleAnalysis
        },
        'meta_description': {
            'meta_description': meta_description,
            'analysis': metaDescriptionAnalysis
        },
        'text': {
            'text': text,
            'analysis': textAnalysis
        }
    }

    return results

def text_analysis(text, keyword):

    results = []

    if keyword is "":
        keyword = None

    if text is "":
        text = None

    #check if text exists
    if text is not None:
        results.append({
            'status': "Valid",
            'message': "The text has been added to the page."
        })
    elif text is None:
        results.append({
            'status': "Invalid",
            'message': "Enter the text to insert on the page."
        })

    #check length of text
    if text is not None:
        if 300 <= len(text):
            results.append({
                'status': "Valid",
                'message': "The length of the text is perfect."
            })

        if 300 > len(text):
            characters_to_use = 300 - len(text)
            results.append({
                'status': "Invalid",
                'message': "Text length is too short, use at least {} charachters".format(characters_to_use)
            })

    else:
        results.append({
            'status': "Invalid",
            'message': "Text length is too short, use at least 300 characters."
        })

    #check if first paragraph of a text contains keyword
    if text is not None:
        if keyword is not None:
            if keyword.lower() in text.lower().partition('.')[0] + '.':
                results.append({
                    'status': "Valid",
                    'message': "The first sentence of the text contains a key phrase."
                })
            elif keyword.lower() in text.lower().partition('.')[0] + '?':
                results.append({
                    'status': "Valid",
                    'message': "The first sentence of the text contains a key phrase."
                })
            elif keyword.lower() in text.lower().partition('.')[0] + '!':
                results.append({
                    'status': "Valid",
                    'message': "The first sentence of the text contains a key phrase."
                })
            else:
                results.append({
                    'status': "Invalid",
                    'message': "The first sentence of the text does not contain a key phrase."
                })
        else:
            results.append({
                'status': "Invalid",
                'message': "Enter a keyword or phrase."
            })
    else:
        results.append({
            'status': "Invalid",
            'message': "The first sentence of the text does not contain a key phrase."
        })

    #check if keyword exists minimum of 3 times
    if text is not None:
        if keyword is not None:
            len_keys_in_text = len([m.start() for m in finditer(r'(?={})'.format(escape(keyword)), text)])
            if len_keys_in_text >= 3:
                results.append({
                    'status': "Valid",
                    'message': "The key phrase occurs frequently."
                })
            else:
                minimum_keys_in_text = 3 - len_keys_in_text
                results.append({
                    'status': "Invalid",
                    'message': "The key phrase is too rare, use it at least {} times.".format(minimum_keys_in_text)
                })
        else:
            results.append({
                'status': "Invalid",
                'message': "The key phrase is too rare, use it at least 3 times."
            })
    else:
        results.append({
            'status': "Invalid",
            'message': "The key phrase is too rare, use it at least 3 times."
        })

    undefined_results = [{
        "status": "Undefined",
        "message_h1_exists": "Remember to add the h1 tag at least once."
    },
    {
        "status": "Undefined",
        "message_h2_exists": "Remember to add the h2 tag at least three times."
    },
    {
        "status": "Undefined",
        "message_links_exists": "Remember to add at least one internal and external link."
    },
    {
        "status": "Undefined",
        "message_image_exists": "Remember to add a photo at least three times."
    }]

    #append data independent of the content analyzer
    for result in undefined_results:
        results.append(result)

    return results

def keyword_analysis(keyword):

    results = []

    if keyword is "":
        keyword = None

    #check if keyword exists
    if keyword is not None:
        if (' ' in keyword) == True:
            results.append({
                'status': "Valid",
                'message': "A keyword has been entered."
            })
        elif (' ' not in keyword) == True:
            results.append({
                'status': "Vaild",
                'message': "A keyword has been entered."
            })

        #check if keyword has proper len
        if len(keyword) < 60:
            results.append({
                'status': "Valid",
                'message': "The key phrase is of the right length."
            })
        else:
            characters_to_remove = len(keyword) - 60
            results.append({
                'status': "Invalid",
                'message': "The key phrase is too long. Reduce it by at least {} charachters.".format(characters_to_remove)
            })

    elif keyword is None:
        results.append({
            'status': "Invalid",
            'message': "Enter a phrase or keyword."
        })

        results.append({
            'status': "Invalid",
            'message': "The key phrase is too short."
        })

    return results

def title_analysis(keyword, page_title):

    results = []

    if keyword is "":
        keyword = None

    if page_title is "":
        page_title = None

    #check if keyword exists in page_title
    if page_title is not None:
        if keyword is not None:
            if page_title.count(keyword):
                results.append({
                    'status': "Valid",
                    'message': "The key phrase is in the page name."
                })
            else:
                results.append({
                    'status': "Invalid",
                    'message': "The key phrase is not in the page name."
                })
        elif keyword is None:
            results.append({
                'status': "Invalid",
                'message': "Enter a phrase or keyword."
            })
    elif page_title is None:
        results.append({
            'status': "Invalid",
            'message': "Enter the page name."
        })

    #check if page title starts with keyword
    if page_title is not None:
        if keyword is not None:
            if page_title.startswith(keyword):
                results.append({
                    'status': "Valid",
                    'message': "The key phrase appears at the beginning of the sentence."
                })
            else:
                results.append({
                    'status': "Invalid",
                    'message': "The key phrase does not appear at the beginning of the sentence."
                })
        elif keyword is None:
            results.append({
                'status': "Invalid",
                'message': "Enter a phrase or keyword."
            })
    elif page_title is None:
        results.append({
            'status': "Invalid",
            'message': "Enter the page name."
        })

    #check the length of page_title
    if page_title is not None:
        if 30 <= len(page_title) <= 60:
            characters_to_use = 60 - len(page_title)
            results.append({
                'status': "Valid",
                'message': "Page name length is perfect, {} characters available.".format(characters_to_use)
            })

        elif len(page_title) < 30:
            characters_to_use = len(page_title) - 30
            results.append({
                'status': "Invalid",
                'message': "Page name length is too short, add at least {} characters.".format(characters_to_use)
            })

        elif len(page_title) > 60:
            characters_to_use = len(page_title) - 60
            results.append({
                'status': "Invalid",
                'message': "The length of the page name is too long, shorten it by at least {} characters.".format(characters_to_use)
            })

    elif page_title is None:
        results.append({
            'status': "Invalid",
            'message': "Enter the page name."
        })

    return results

def meta_description_analysis(keyword, meta_description):

    results = []

    if keyword is "":
        keyword = None

    if meta_description is "":
        meta_description = None

    #check if keyword exists in meta description
    if meta_description is not None:
        if keyword is not None:
            if (' ' in keyword) == True:
                number_of_keywords = keyword.split()
                for keywords in number_of_keywords:
                    if keywords.lower() in meta_description.lower():
                        results.append({
                            'status': "Valid",
                            'message': "The key phrase is in the meta description."
                        })
                    elif keywords.lower() not in meta_description.lower():
                        results.append({
                            'status': "Invalid",
                            'message': "The key phrase does not appear in the meta description."
                        })
                        break
            elif (' ' not in keyword) == True:
                if keyword.lower() in meta_description.lower():
                    results.append({
                        'status': "Valid",
                        'message': "The keyword is in the meta description."
                    })
                elif keyword.lower() not in meta_description.lower():
                    results.append({
                        'status': "Invalid",
                        'message': "The keyword is not in the meta description."
                    })
        elif keyword is None:
            results.append({
                'status': "Invalid",
                'message': "Enter a phrase or keyword."
            })
    elif meta_description is None:
        results.append({
            'status': "Invalid",
            'message': "Enter a meta description."
        })

    #check length of meta_description
    if meta_description is not None:
        if 155 <= len(meta_description) <= 160:
            characters_to_use = 160 - len(meta_description)
            results.append({
                'status': "Valid",
                'message': "Meta description length is perfect, {} characters available.".format(characters_to_use)
            })

        elif 100 <= len(meta_description) < 155:
            characters_to_use = 155 - len(meta_description)
            results.append({
                'status': "Valid",
                'message': "Meta description length is fine, add at least {} characters to make it perfect.".format(characters_to_use)
            })

        elif len(meta_description) < 100:
            characters_to_use = 100 - len(meta_description)
            results.append({
                'status': "Invalid",
                'message': "Meta description length is too short, add at least {} charachters".format(characters_to_use)
            })

        elif len(meta_description) > 160:
            characters_to_use = len(meta_description) - 160
            results.append({
                'status': "Invalid",
                'message': "The length of the meta description is too long, shorten it by at least {} charachters.".format(characters_to_use)
            })

    elif meta_description is None:
        results.append({
            'status': "Invalid",
            'message': "Enter a meta description."
        })

    return results
