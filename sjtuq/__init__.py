'''SJTU Questionnaire data retrieval and processing

@author: Kunologist
'''

from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import logging
import json


class SJTUQuestionnaire():
    '''An SJTU Questionnaire class for Object-Oriented Programming

    @cvar sjtu_questionnaire_api_format: The format of the SJTU Questionnaire API, currently supports SJTU Questionnaire API v1
    @type sjtu_questionnaire_api_format: str
    @ivar url: The base URL of the SJTU Questionnaire API
    @type url: str
    @ivar has_logger: Whether the SJTU Questionnaire object has a logger
    @type has_logger: bool
    @ivar logger: The logger of the SJTU Questionnaire object, can be None if not provided
    @type logger: logging.Logger or None
    '''
    sjtu_questionnaire_api_format_url = "https://wj.sjtu.edu.cn/api/v1/public/result/{key}/json"

    def __init__(self, url_or_key: str, logger: logging.Logger = None):
        '''Initialize an SJTU Questionnaire object

        @param url_or_key: The URL of the SJTU Questionnaire API or the key of the SJTU Questionnaire API
        @type url_or_key: str
        
        If C{url_or_key} starts with "https://wj.sjtu.edu.cn/api/v1/public/", it is assumed to be a URL.

        If C{url_or_key} has length 32 and is a hexadecimal string, it is assumed to be a key of the SJTU Questionnaire API. The key will be converted to a URL using the C{sjtu_questionnaire_api_format} class variable.
        
        @param logger: The logger of the SJTU Questionnaire object, can be None if not provided
        @type logger: logging.Logger or None
        '''
        if isinstance(url_or_key, str) and url_or_key.startswith("https://wj.sjtu.edu.cn/api/v1/public/"):
            self.url = url_or_key
        elif isinstance(url_or_key, str) and len(url_or_key) == 32 and all(c in "0123456789abcdef" for c in url_or_key):
            self.url = SJTUQuestionnaire.sjtu_questionnaire_api_format_url.format(key=url_or_key)
        elif isinstance(url_or_key, str):
            raise ValueError("Invalid url_or_key: {}".format(url_or_key))
        else:
            raise TypeError("url_or_key must be a string, but got {}".format(type(url_or_key)))
        if isinstance(logger, logging.Logger):
            self.logger = logger
            self.has_logger = True
        elif logger is None:
            self.logger = logger
            self.has_logger = logger is not None
        else:
            raise TypeError("logger must be a logging.Logger object, but got {}".format(type(logger)))

    def __log(self, msg: str, level: int = logging.DEBUG):
        if self.has_logger:
            self.logger.log(level, msg)

    def get_data(self, params: dict = None, sort: str = "asc") -> dict:
        '''Send a request to SJTU Questionnaire API. This is just a wrapper for C{requests.get}. It is the developer's responsibility to check the validity, usually whether C{ret["success"]} is C{True}.

        @param params: The parameters of the SJTU Questionnaire API, defaults to None (treated as an empty dict).
        @type params: dict or None
        @param sort: The sort of the SJTU Questionnaire API, defaults to "asc". It can be "asc" or "desc".
        @return: Response of the SJTU Questionnaire API
        @rtype: dict
        
        For bad response by the server (determined by status code), there will be no exception raised, but the error info will be logged to logger and returned as-is.
        
        @raise ValueError: If either params or sort is invalid.
        @raise requests.exceptions.RequestException: If the request fails.
        @note: See L{get_all_data} if you would like to get all the data without bothering about pagination.
        '''
        # Type and value check
        if params is None:
            self.__log("params not specified, defaults to an empty dict", level=logging.DEBUG)
            params = {}
        elif not isinstance(params, dict):
            self.__log("params must be a dict, but got {}".format(type(params)), logging.ERROR)
            raise ValueError("params must be a dict, but got {}".format(type(params)))
        if sort not in ("asc", "desc"):
            self.__log("sort must be either \"asc\" or \"desc\", but got {}".format(sort), logging.ERROR)
            raise ValueError("Invalid sort, must be \"asc\" or \"desc\", but got \"{}\"".format(sort))
        # Check params key
        # TODO

        # Build request parameters
        real_params = {
            "sort": json.dumps({"id": sort}),
            "params": json.dumps(params)
        }

        # Send request
        response = requests.get(self.url, params=real_params)
        self.__log("Sending GET request to {}".format(response.url))
        if response.status_code != 200:
            self.__log("Error: Status code {} in get_data".format(response.status_code), level=logging.ERROR)
            self.__log("       Response: {}".format(response.text), level=logging.ERROR)
        return response.json()

    def get_all_data(self, params: dict = None, sort: str = "asc", max_workers: int = None) -> list:
        '''Get all the data of the questionnaire. This will send multiple requests to the server, and the data will be merged into a list of user answers.

        @param params: The parameters of the SJTU Questionnaire API, defaults to None (treated as an empty dict).
        @type params: dict or None
        
        Some values will be overridden, such as C{pageSize} and C{current}.
        
        @param sort: The sort of the SJTU Questionnaire API, defaults to "asc". It can be "asc" or "desc".
        @param max_workers: The maximum number of concurrent threads, defaults to None (uses ThreadPoolExecutor default, typically min(32, cpu_count + 4)).
        @type max_workers: int or None
        @return: All the data of the SJTU Questionnaire API
        @rtype: list

        For bad response by the server (determined by status code), an empty list C{[]} will be returned, and the error will be logged.

        @raise ValueError: If either params or sort is invalid.
        @raise requests.exceptions.RequestException: If the request fails.
        '''
        # Type and value check
        if params is None:
            self.__log("params not specified, defaults to an empty dict", level=logging.DEBUG)
            params = {}
        elif not isinstance(params, dict):
            self.__log("params must be a dict, but got {}".format(type(params)), level=logging.ERROR)
            raise ValueError("params must be a dict, but got {}".format(type(params)))
        if sort not in ("asc", "desc"):
            self.__log("Invalid sort, must be \"asc\" or \"desc\", but got \"{}\"".format(sort), level=logging.ERROR)
            raise ValueError("Invalid sort, must be \"asc\" or \"desc\", but got \"{}\"".format(sort))
        
        # Check params key
        if "pageSize" in params:
            self.__log("pageSize will be overridden", level=logging.WARNING)
        if "current" in params:
            self.__log("current will be overridden", level=logging.WARNING)
        
        # First check the total number of data
        params_copy = deepcopy(params)
        params_copy["pageSize"] = 1  # To minimize the response package size
        params_copy["current"] = 1
        response = self.get_data(params_copy, sort=sort)
        if not ("success" in response and response["success"]):
            self.__log("Error: Failed to get the total number of data", level=logging.ERROR)
            return []
        total = response["data"]["total"]
        self.__log("Total number of rows: {}".format(total))

        if total == 0:
            return []

        # Calculate number of pages needed
        page_size = 100
        page_count = (total + page_size - 1) // page_size  # Ceiling division

        # Build independent param dicts for each page to avoid race conditions
        tasks = []
        for page_num in range(1, page_count + 1):
            task_params = deepcopy(params)
            task_params["pageSize"] = page_size
            task_params["current"] = page_num
            tasks.append((page_num, task_params))

        self.__log("Fetching {} pages with ThreadPoolExecutor (max_workers={})".format(
            page_count, max_workers or "default"))

        # Use ThreadPoolExecutor for concurrent I/O-bound requests
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_page = {
                executor.submit(self.get_data, task_params, sort): page_num
                for page_num, task_params in tasks
            }
            for future in as_completed(future_to_page):
                page_num = future_to_page[future]
                try:
                    resp = future.result()
                    if resp.get("success") and "data" in resp:
                        results[page_num] = resp["data"]["rows"]
                    else:
                        self.__log("Error: Failed to get data for page {}".format(page_num), level=logging.ERROR)
                        results[page_num] = []
                except Exception as e:
                    self.__log("Exception on page {}: {}".format(page_num, e), level=logging.ERROR)
                    results[page_num] = []

        # Merge results in correct page order
        data = []
        for page_num in range(1, page_count + 1):
            data.extend(results.get(page_num, []))

        return data
