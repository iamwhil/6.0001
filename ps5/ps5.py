# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    """
    A formatted news story fed in from a parsed RSS feed."""
    
    def __init__(self, guid, title, description,link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhaseTrigger(Trigger):
    """ 
    Returns True if the phrase is found in the given text.
    """
    def __init__(self, phrase):
        self.phrase = phrase.lower()
        
    def get_phrase(self):
        return self.phrase
        
    def is_phrase_in(self, text):
        text = text.lower()
        for p in string.punctuation:
            text = text.replace(p, ' ')
        text = text.split()
        phrase_list = self.get_phrase().split()
        
        # Testing with list comprehension
        # This does not work, this checks each element in the list against the other list elemenets.
        #t_f = [True for x in [1, 2, 3] if x in [1, 2, 3, 4]]
        
        # Also just using `string in string` does not work as multiple cases are included (cow vs cows).
        
        count = 0 # Count the number of words in the phrase found consecutively in the text.
        for i in range(len(text)):
            if text[i] == phrase_list[count]:
                count += 1
                if count == len(phrase_list):
                    return True
            else:
                count = 0
        return False
        
# Problem 3
class TitleTrigger(PhaseTrigger):
    """ Returns true if the phrase is found in the Story's title."""
    def __init__(self, phrase):
        PhaseTrigger.__init__(self, phrase)
        
    def evaluate(self, story):
        if self.is_phrase_in(story.get_title()):
            return True
        else:
            return False

# Problem 4
class DescriptionTrigger(PhaseTrigger):
    """ Returns true if the phrase is found in the Story's description."""
    def __init__(self, phrase):
        PhaseTrigger.__init__(self, phrase)
        
    def evaluate(self, story):
        if self.is_phrase_in(story.get_description()):
            return True
        else:
            return False
        

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    """
    takes a time in EST in the format of %d %b %Y %H:%M:%S
    
    Returns a formatted datetime object.
    """
    def __init__(self, trigger_time):
        self.time = self.format_trigger_time(trigger_time)
        
    def get_time(self):
        return self.time
        
    def format_trigger_time(self, trigger_time):
        formatted_time = datetime.strptime(trigger_time, "%d %b %Y %H:%M:%S")
        formatted_time = formatted_time.replace(tzinfo=pytz.timezone("EST"))
        return formatted_time

# Problem 6
class BeforeTrigger(TimeTrigger):
    """Returns true if the story occurs before the time trigger."""
    def __init__(self, trigger_time):
        TimeTrigger.__init__(self, trigger_time)
        
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        trigger_time = self.get_time()
        if pubdate.tzname() is None:
            pubdate = pubdate.replace(tzinfo=None)
            trigger_time = trigger_time.replace(tzinfo=None)
        if pubdate < trigger_time:
            return True
        else:
            return False
        
class AfterTrigger(TimeTrigger):
    """Returns true if the story occurs after the time trigger."""
    def __init__(self, trigger_time):
        TimeTrigger.__init__(self, trigger_time)
        
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        trigger_time = self.get_time()
        if pubdate.tzname() is None:
            pubdate = pubdate.replace(tzinfo=None)
            trigger_time = trigger_time.replace(tzinfo=None)
        if pubdate > trigger_time:
            return True
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    """Returns not trigger.evaluate(story)."""
    def __init__(self, T):
        self.trigger = T
#        
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    """Returns true if triggers both fire as true."""
    def __init__(self, t1, t2):
        self.trigger1 = t1
        self.trigger2 = t2
        
    def evaluate(self, story):
        if self.trigger1.evaluate(story) and self.trigger2.evaluate(story):
            return True
        else:
            return False

# Problem 9
class OrTrigger(Trigger):
    """Returns true if either trigger fires as true."""
    def __init__(self, t1, t2):
        self.trigger1 = t1
        self.trigger2 = t2
    
    def evaluate(self, story):
        if self.trigger1.evaluate(story) or self.trigger2.evaluate(story):
            return True
        else:
            return False


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = [] # List to hold stories when the trigger fires.
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
    
    return filtered_stories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    triggers = {}
    trigger_list = []
    for line in lines:
        trigger_config = line.split(',')
        first_command = trigger_config.pop(0)
        if first_command == "ADD":
            for t in trigger_config:
                trigger_list.append(triggers[t])
        else:
            trigger_type = trigger_config.pop(0)
            triggers[first_command] = trigger_dictionary(trigger_type, trigger_config, triggers)

    return trigger_list
    
def trigger_dictionary(trigger_type, trigger_config, triggers):
    """
    Returns a trigger based on the trigger_type and trigger_config.
    I would have liked to have used a switch or case statement, but
    it seems Python does not have that baked in.
    Instead people use dictionaries.  However the dictionary would have
    still had many if statements to check if the trigger_config was
    of the correct format, so a single if elif else statement was used."""
    
    if trigger_type == "TITLE":
        return TitleTrigger(trigger_config[0])
    elif trigger_type == "DESCRIPTION":
        return TitleTrigger(trigger_config[0])
    elif trigger_type == "AFTER":
        return AfterTrigger(trigger_config[0])
    elif trigger_type == "BEFORE":
        return BeforeTrigger(trigger_config[0])
    elif trigger_type == "OR":
        return OrTrigger(triggers[trigger_config[0]], triggers[trigger_config[1]])
    elif trigger_type == "AND":
        return AndTrigger(triggers[trigger_config[0]], triggers[trigger_config[1]])
    elif trigger_type == "NOT":
        return NotTrigger(triggers[trigger_config[0]])
    else:
        return None


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    """ Runs the main program loading triggers.txt to find news items in the google and yahoo rss feeds."""
    try:

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

