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

    def Copy(self):
        copy = BoardState()
        
        for thread_num, headline in self.headlines.iteritems():
            copy.headlines[thread_num] = headline.Copy()
            
        return copy    
    
    def Diff(self, other):
        """Generate a diff between two board states.
        
        Example:
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
    
    def Union(self, other):
        """Create a merge this board state with another state.
        
        Example:
            # Mark as read
            last_read =  last_read.Union(last_recieved)
        """
        union_headlines = self.headlines.copy()
        union_headlines.update(other.headlines)
                
        # Let's not steal any references
        for thread_num, headline in self.headlines.iteritems():
            self.headlines[thread_num] = headline.Copy()
        
        union_board_state = BoardState()
        union_board_state.headlines = union_headlines
        
        return union_board_state 


class BoardStateDiff(object):
    """A diff between a board at different times."""
    def __init__(self, new_thread_nums, deleted_thread_nums, num_new_posts):
        self.new_thread_nums = new_thread_nums
        self.deleted_thread_nums = deleted_thread_nums
        self.num_new_posts = num_new_posts
