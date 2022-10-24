'''param.py

@note: This file contains query parameter class for SJTU Questionnaire.

@author: Kunologist
'''
import json
from typing import List, Union
from .question import Question

class QuestionFilter():
    '''
    Bases on a question with a specified answer filter.
    '''
    def __init__(self, question: Union[Question, str], answer: Union[int, float, str, List[str]]):
        '''
        @param question: The question to be filtered
        @type question: Question
        @param answer_filter: The answer filter
        @type answer_filter: List[str]
        '''
        # Type check
        if not isinstance(question, (Question, str)):
            raise TypeError("question must be a Question object or a string, but got {}".format(type(question)))
        if not isinstance(answer, (int, float, str, list)):
            raise TypeError("answer must be a int, float, str or list, but got {}".format(type(answer)))
        if isinstance(answer, list) and not all(isinstance(a, str) for a in answer):
            raise TypeError("answer must be a list of strings, but got {}".format(answer))
        self.question = question
        self.answer_filter = answer
    def get_id(self) -> str:
        '''
        Get the ID of the question to be filtered.
        '''
        if isinstance(self.question, Question):
            return self.question.get_id()
        elif isinstance(self.question, str):
            return self.question
    def get_answer(self) -> Union[int, float, str, List[str]]:
        '''
        Get the answer filter.
        '''
        return self.answer_filter

class Param():
    '''
    Query parameters for SJTU Questionnaire.

    @cvar current: The current page.
    @cvar page_size: The page size of the query. Must be smaller than 100.
    @cvar account: Filter results by the specific username.
    @cvar user_organization: Filter results by a specific organization.
    @cvar by_question: Filter the results by the answer to a specific question.
    '''
    def __init__(self,
                 current: int=0,
                 page_size: int=20,
                 account: str=None,
                 user_organization: str=None,
                 by_question: List[QuestionFilter]=None):
        '''
        Initialize a Param object.
        
        @param current: The current page
        @type current: int
        @param page_size: The page size of the query
        @type page_size: int
        @param account: Filter results by the specific username
        @type account: str
        @param user_organization: Filter results by a specific organization
        @type user_organization: str
        @param by_question: Filter the results by the answer to a specific question
        @type by_question: dict
        '''
        # Check the type of the parameters
        if not isinstance(current, int):
            raise TypeError("current must be an integer, but got {}".format(type(current)))
        if not isinstance(page_size, int):
            raise TypeError("page_size must be an integer, but got {}".format(type(page_size)))
        if account is not None and not isinstance(account, str):
            raise TypeError("account must be a string, but got {}".format(type(account)))
        if user_organization is not None and not isinstance(user_organization, str):
            raise TypeError("user_organization must be a string, but got {}".format(type(user_organization)))
        if by_question is not None and not isinstance(by_question, list):
            raise TypeError("by_question must be a list, but got {}".format(type(by_question)))
        # Check the value of the parameters
        if current < 0:
            raise ValueError("current must be a positive integer, but got {}".format(current))
        if page_size < 0 or page_size > 100:
            raise ValueError("page_size must be a positive integer smaller than 100, but got {}".format(page_size))
        if by_question is not None and not all(isinstance(q, QuestionFilter) for q in by_question):
            raise TypeError("by_question must be a list of QuestionFilter objects, but got {}".format(by_question))
        # Set the parameters
        self.current = current
        self.page_size = page_size
        self.account = account
        self.user_organization = user_organization
        self.by_question = by_question
    
    def to_json(self) -> str:
        '''
        Convert the Param object to a JSON string.
        
        @return: The JSON string
        @rtype: str
        '''
        return json.dumps({
            "current": self.current,
            "pageSize": self.page_size,
            "account": self.account,
            "user_organization": self.user_organization,
            **{q.get_id(): q.get_answer() for q in self.by_question}
        })

class Sort():
    '''
    Sort parameters for SJTU Questionnaire.

    @cvar id: Sort by the ID of the questionnaire. Defaults to "asc", but can be set to "desc" by passing C{True} to the constructor.
    '''
    def __init__(self, should_desc: bool=False):
        '''
        Specify the sort method. Defaults to "asc", but can be set to "desc" by passing C{True} to the constructor.

        @param should_desc: Whether the sort method should be descending
        @type should_desc: bool
        '''
        self.id = "desc" if should_desc else "asc"
    def to_json(self) -> dict:
        '''
        Convert the Sort object to a JSON object.

        @return: The JSON object
        @rtype: dict
        '''
        return {"id": self.id}

class Query():
    '''
    A query is an object that contains a Param class and a Sort class, and is passed directly to SJTU Questionnaire API.
    '''
    def __init__(self, param: Param, sort: Sort):
        '''
        Initialize a query object.
        
        @param param: The Param object
        @type param: Param
        @param sort: The Sort object
        @type sort: Sort
        '''
        self.param = param
        self.sort = sort
    def set_param(self, param: Param):
        '''
        Set the Param object.
        
        @param param: The Param object
        @type param: Param
        '''
        if not isinstance(param, Param):
            raise TypeError("param must be a Param object, but got {}".format(type(param)))
        self.param = param
    def set_sort(self, sort: Sort):
        '''
        Set the Sort object.
        
        @param sort: The Sort object
        @type sort: Sort
        '''
        if not isinstance(sort, Sort):
            raise TypeError("sort must be a Sort object, but got {}".format(type(sort)))
        self.sort = sort
    def get_param(self) -> Param:
        '''
        Get the Param object.
        
        @return: The Param object
        @rtype: Param
        '''
        return self.param
    def get_sort(self) -> Sort:
        '''
        Get the Sort object.
        
        @return: The Sort object
        @rtype: Sort
        '''
        return self.sort
    def to_json(self) -> str:
        '''
        Convert the query object to a JSON string.
        
        @return: The JSON string
        @rtype: str
        '''
        return json.dumps({"params": self.param.to_json(), "sort": self.sort.to_json()})
