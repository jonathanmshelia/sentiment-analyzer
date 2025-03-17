from typing import List
from scraper.Comment import Comment

class RawCommentParser:
    def __init__(self):
        self.comments = []

    def parse_comments(self, data: dict) -> List[Comment]:
        """Parse comments from Reddit API response"""
        self.comments = []
        
        # Reddit API returns two listings: post and comments
        if len(data) >= 2 and 'data' in data[1]:
            comments_data = data[1]['data']
            if 'children' in comments_data:
                for child in comments_data['children']:
                    if child['kind'] == 't1':  # t1 is comment type
                        comment_data = child['data']
                        comment = self._create_comment_from_json(comment_data)
                        self.comments.append(comment)
                        
                        # Parse replies if they exist
                        if 'replies' in comment_data and comment_data['replies']:
                            if isinstance(comment_data['replies'], dict) and 'data' in comment_data['replies']:
                                self._parse_replies(comment_data['replies']['data']['children'], comment)
        
        return self.comments
    
    def _parse_replies(self, replies_data, parent_comment) -> None:
        """Recursively parse nested replies"""
        for reply in replies_data:
            if reply['kind'] == 't1':
                reply_data = reply['data']
                reply_comment = self._create_comment_from_json(reply_data)
                parent_comment.children.append(reply_comment)
                
                # Recursively parse nested replies
                if 'replies' in reply_data and reply_data['replies']:
                    if isinstance(reply_data['replies'], dict) and 'data' in reply_data['replies']:
                        self._parse_replies(reply_data['replies']['data']['children'], reply_comment)

    def _create_comment_from_json(self, data: dict) -> Comment:
        return Comment(
            _id=data.get('id', ''),
            author=data.get('author', ''),
            body=data.get('body', ''),
            created_utc=data.get('created_utc', 0),
            score=data.get('score', 0),
            parent_id=data.get('parent_id', None),
            depth=data.get('depth', 0),
            ups=data.get('ups', 0),
            downs=data.get('downs', 0),
            num_reports=data.get('num_reports', None),
            report_reasons=data.get('report_reasons', None),
            children=[]
        )
