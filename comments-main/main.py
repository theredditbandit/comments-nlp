import re
from os import path
from colorama import Fore as c
from googleapiclient.discovery import build
from tqdm import tqdm
import csv
from sys import exit


def validateApi(key: str) -> None:
    """_summary_ : to validate the user input."""
    if key:
        pass
    else:
        exitProg("API key Invalid! ❌", 1)
    youtube = build("youtube", "v3", developerKey=key)
    request = youtube.commentThreads().list(
        part="id", maxResults=0, videoId="fT2KhJ8W-Kg"
    )
    try:
        for _ in tqdm(range(5), desc="Validating API key . . ."):
            request.execute()
    except Exception:
        exitProg(f"API key {key} is invalid! ❌", 1)
    else:
        print("API Key is Valid ✔️")


def getKey():
    """_summary_ : Function to prompt the user for their API key

    Returns:
        string : The api key
    """
    API_KEY = ""
    if path.isfile(".env"):
        with open(".env") as env:
            API_KEY = env.readline()
        print(c.GREEN + "Got API KEY! ✔️")
    else:
        print(
            c.YELLOW
            + "You can get your API key from : "
            + c.BLUE
            + "https://console.cloud.google.com/apis/library/youtube.googleapis.com"
        )
        API_KEY = input(c.WHITE + "Enter API Key (Use Ctrl+Shift+V to paste):")
        validateApi(API_KEY)
        print(c.GREEN + "Saving API key . . " + c.WHITE + ". ")
        with open(".env", "w") as env:
            env.write(API_KEY)
    return API_KEY


def theInput():
    return input(c.LIGHTBLUE_EX + "Enter a Youtube URL >" + c.WHITE + "> ")


def isvalid(url):
    """_summary_ : Validate whether the given url belongs to a youtube video or not

    Args:
        url (_str_): The video url

    Returns:
        _bool_
    """
    global regex
    regex = r"https:\/\/(?:youtu\.be\/|www\.youtube\.com\/watch\?v=)([^&#]+)"
    if re.search(regex, url):
        return True
    else:
        print(
            c.RED + "Please enter the URL to a Youtube Video ",
            c.WHITE + "Example : https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            sep="\n",
        )
        return False


def getId(url):
    """_summary_ : Extract video ID from the youtube URL for the youtube API

    Args:
        url (_str_): The video url
    Returns: The video id
    """
    id = re.search(regex, url).group(1)
    print(c.LIGHTGREEN_EX + "Video ID Found : " + c.WHITE + id)
    return id


def exitProg(reason="", code=0):
    if reason:
        print(c.RED + reason)

    print(c.RED + "\nExiting the Program . . " + c.WHITE + ".")
    exit(code)


def getComments(API_KEY, vidId, results=20, allComments=False):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    part = "id,snippet"

    def getComments():
        request = youtube.commentThreads().list(
            part=part, maxResults=results, order="time", videoId=vidId
        )
        for _ in tqdm(range(10), desc=c.GREEN + "Fetching  Comments . . ."):
            response = request.execute()
        #  format the response dict to return a list of comments

        with open(f"{vidId}_comments.csv", "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Author", "Likes", "Comment"])

            for comment in response["items"]:
                writer.writerow(
                    [
                        comment["snippet"]["topLevelComment"]["snippet"][
                            "authorDisplayName"
                        ],
                        comment["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                        comment["snippet"]["topLevelComment"]["snippet"][
                            "textOriginal"
                        ],
                    ]
                )
        print(
            c.GREEN + "Comments saved to file " +
            c.WHITE + f"{vidId}_comments.csv ✔️"
        )

    def getAllComments():
        next_page_token = ""
        with open(f"{vidId}_comments.csv", "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Author", "Likes", "Comment"])
            for _ in tqdm(range(100), desc=c.GREEN + "Fetching  All Comments . . ."):
                while True:
                    request = youtube.commentThreads().list(
                        part=part,
                        maxResults=results,
                        order="time",
                        videoId=vidId,
                        pageToken=next_page_token,
                    )
                    response = request.execute()
                    for comment in response["items"]:
                        writer.writerow(
                            [
                                comment["snippet"]["topLevelComment"]["snippet"][
                                    "authorDisplayName"
                                ],
                                comment["snippet"]["topLevelComment"]["snippet"][
                                    "likeCount"
                                ],
                                comment["snippet"]["topLevelComment"]["snippet"][
                                    "textOriginal"
                                ],
                            ]
                        )
                    next_page_token = response.get("nextPageToken", None)
                    if not next_page_token:
                        break

    if allComments or results > 100:
        getAllComments()
    else:
        getComments()


def getNumberOfComments():
    try:
        results = int(
            input(
                c.YELLOW
                + "Enter the number of results you want to request (max is 100)"
                + c.WHITE
                + ": "
            )
        )
    except Exception:
        print(c.RED + "Invalid character")
        print(c.YELLOW + "Taking the default value as 20")
        results = 20

    return results


def downloadComments():
    API_KEY = getKey()
    while True:
        URL = theInput()
        if isvalid(URL):
            break
        else:
            continue

    id = getId(URL)
    allComments = input(
        c.YELLOW +
        "Do you want to get all the comments ?[Y/N] " + c.WHITE + ": "
    )
    if allComments.upper() == "N":
        allComments = False
        results = getNumberOfComments()
    elif allComments.upper() == "Y":
        allComments = True
        results = 100
    else:
        exitProg("Invalid Choice!")

    getComments(API_KEY, id, results, allComments)


if __name__ == "__main__":
    try:
        downloadComments()
    except KeyboardInterrupt as k:
        exitProg()
