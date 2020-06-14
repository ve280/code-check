/*
 * This is VE280 Project 2, SU2020.
 * Written by Ziqiao Ma and Zhuoer Zhu.
 * Latest Update: 5/23/2020.
 * All rights reserved.
 */

#ifndef SERVER_TYPE_H
#define SERVER_TYPE_H

#include <string>

using namespace std;


/* Constants */

// Max number of users in the server
const unsigned int MAX_USERS = 20;

// Max number of followers per user
const unsigned int MAX_FOLLOWERS = 20;

// Max number of following per user
const unsigned int MAX_FOLLOWING = 20;

// Max number of posts per user
const unsigned int MAX_POSTS = 50;

// Max number of comments per post
const unsigned int MAX_COMMENTS = 50;

// Max number of tags per post
const unsigned int MAX_TAGS = 5;

// Max number of likes per post
const unsigned int MAX_LIKES = 20;

/* Exception */
enum Error_t {
    INVALID_ARGUMENT,
    FILE_EXIST,
    CAPACITY_OVERFLOW,
    INVALID_LOG,
};

struct Exception_t: public exception{
    Error_t error;
    string error_info;

    Exception_t(Error_t err, const string& info){
        this->error = err;
        this->error_info = info;
    }
};


/* Compound Types Declaration */

struct Comment_t;
struct Tag_t;
struct Post_t;
struct User_t;

/* TODO: Declare any additional compound types here */
struct Server_t;

/* Compound Types Definition */

struct Comment_t
/*
// Type: Comment_t
// ------------------
// The type Comment_t is used to represent a comment
// It consists of:
// * text: text of comment
// * user: pointer to the user who posted that comment
*/
{
    string text;
    User_t *user;
};


struct Tag_t
/*
// Type: Tag_t
// ------------------
// The type Tag_t is used to represent a tag
// It consists of:
// * tag_content: the content of the tag
// * tag_score: the score of the tag used to determine the trend
// COMMENT: can either use num_relatedPost or score to detect whether it's last tag in the post of this server
// * num_relatedPost: the number of the post this tag related to
*/
{
    string tag_content;
    unsigned int tag_score;
    unsigned int num_relatedPost;
};


struct Post_t
/*
// Type: Post_t
// ------------------
// The type Comment_t is used to represent a post
// It consists of:
// * comments: An array of comments
// * like_users: An array of pointers to the users who like this post
// * tagContents: An array of tag contents of this post
// * owner: A pointer to the post owner
// * title: the title of the post
// * text: the text of the post
// * num_likes: the number of likes
// * num_comments: the number of comments
*/
{
    Comment_t comments[MAX_COMMENTS];
    User_t *like_users[MAX_USERS];
    string tagContents[MAX_TAGS];
    User_t *owner;
    string title;
    string text;
    unsigned int num_likes;
    unsigned int num_comments;
    unsigned int num_tag;
};


struct User_t
/*
// Type: User_t
// ------------------
// The type Comment_t is used to represent a user
// It consists of:
// * posts: An array of posts
// * following: An array of following usernames
// * follower: An array of followers
// * name: the username of user
// * num_posts: the number of posts
// * num_following: the number of following users
// * num_follower: the number of followers
*/
{
    Post_t posts[MAX_POSTS];
    User_t *following[MAX_FOLLOWING];
    User_t *follower[MAX_FOLLOWERS];
    string username;
    unsigned int num_posts;
    unsigned int num_following;
    unsigned int num_followers;
};

/* TODO: Define any additional compound types here */
// Hint: You might find a driver structure "Server_t" useful.

struct Server_t
/*
// Type: Server_t
// ------------------
// The type Server_t is used to represent a server managing the whole system
// It consists of:
// * users: An array of users
// * tagSet: An set of tags
// * num_users: the number of users
// * num_tags: the number of tags
*/
{
    User_t users[MAX_USERS];
    Tag_t tagSet[MAX_POSTS* MAX_USERS * MAX_TAGS];
    unsigned int num_users = 0;
    unsigned int num_tags = 0;
};

#endif // SERVER_TYPE_H
