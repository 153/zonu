#!/usr/bin/python 


class BoardState(object):
    
    def __init__(self, board=None):
        if board is None:
            self.headlines = {}
        else:
            if board.headlines is None:
                raise ValueError()
        
            self.headlines = {}
        
            for headline in board.headlines:
                self.headlines[headline.thread_num] = headline

    def Diff(self, other):
        """Generate a diff between two board states.
        
        Examples:
            newer_state.Diff(older_state)
        """
        my_thread_nums = set(self.headlines.keys())
        other_thread_nums = set(other.headlines.keys())

        new_thread_nums = my_thread_nums - other_thread_nums
        deleted_thread_nums = other_thread_nums - my_thread_nums

        my_total_posts = sum([h.num_posts for h in self.headlines.values()])
        other_total_posts = sum([h.num_posts for h in other.headlines.values()])

        num_new_posts = my_total_posts - other_total_posts

        return BoardStateDiff(new_thread_nums, deleted_thread_nums, num_new_posts)
    
    
class BoardStateDiff(object):
    """A diff between a board at different times."""
    def __init__(self, new_thread_nums, deleted_thread_nums, num_new_posts):
        self.new_thread_nums = new_thread_nums
        self.deleted_thread_nums = deleted_thread_nums
        self.num_new_posts = num_new_posts
