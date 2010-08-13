#!/usr/bin/python


from board import Board


class BoardsCache(object):
    """A boards cache that holds a last read and last retrieved board states,
    and provides some common functions for operating between the two.
    """
    def __init__(self):
        self._last_read = {}
        self._last_retrieved = {}

    def get_last_read(self, board_iden):
        return self._last_read.get(board_iden)

    def get_last_retrieved(self, board_iden):
        return self._last_retrieved.get(board_iden)

    def update_last_retrieved(self, board):
        assert isinstance(board, Board)

        new_state = BoardState(board.board_iden, board)

        if board.board_iden in self._last_retrieved:
            self._last_retrieved[board.board_iden].union_update(new_state)
        else:
            self._last_retrieved[board.board_iden] = new_state

        # Fill in read state if does not exist. This will make everything
        # default to be read.
        if self.get_last_read(board.board_iden) is None:
            self._last_read[board.board_iden] = new_state.copy()

    def mark_board_as_read(self, board_iden):
        self._last_read[board_iden] = self._last_retrieved[board_iden].copy()

    def mark_thread_as_read(self, board_iden, thread_num):
        self._last_read[board_iden].headlines[thread_num] = \
            self._last_retrieved[board_iden].headlines[thread_num].copy()

    def gen_diff(self, board_iden):
        """Get a diff between the last read state and the last retrieved state.

        This returns a BoardStateDiff instance.
        """
        if not (board_iden in self._last_read and
                board_iden in self._last_retrieved):
            raise Exception()

        newer = self._last_retrieved[board_iden]
        older = self._last_read[board_iden]

        newer_thread_nums = set(newer.headlines.keys())
        older_thread_nums = set(older.headlines.keys())

        my_total_posts = sum([h.num_posts for h in newer.headlines.values()])
        older_total_posts = sum([h.num_posts for h in older.headlines.values()])

        num_new_posts = my_total_posts - older_total_posts
        num_new_threads = 0

        for thread_num, headline in newer.headlines.iteritems():
            if thread_num in older.headlines:
                if newer.headlines[thread_num].num_posts > older.headlines[thread_num].num_posts:
                    num_new_threads += 1
            else:
                num_new_threads += 1
        
        return BoardStateDiff(board_iden, num_new_posts, num_new_threads)

    def inc_thread_num_posts(self, board_iden, thread_num, n):
        """Increment the number of posts in a thread in read and retrieved states.

        This is useful because after posting it is necessary to increment the read
        state's number of posts by one so we don't think our own posts are new.
        """
        self._last_read[board_iden].headlines[thread_num].num_posts += 1
        self._last_retrieved[board_iden].headlines[thread_num].num_posts += 1
        

class BoardState(object):
    """A class for representing a board state."""

    def __init__(self, board_iden, board=None):
        """Initializes a board state. If board the argument is provided, the state will be read
        from that board's headlines (which means board.GetHeadlines() must have been called).
        """
        self.board_iden = board_iden

        if board is None:
            self.headlines = {}
        else:
            if board.headlines is None:
                raise ValueError()
        
            self.headlines = {}
        
            for headline in board.headlines:
                self.headlines[headline.thread_num] = headline

    def copy(self):
        """Generates a copy of this board state."""
        cp = BoardState(self.board_iden)
        
        for thread_num, headline in self.headlines.iteritems():
            cp.headlines[thread_num] = headline.copy()
            
        return cp
        
    def union_update(self, other):
        """Changes this board state with added data from with another board state.

        Upon the case that a headline is in both states, the one with more
        posts is taken. If they have the same number of posts, there is no
        promise as to which is picked.

        Returns self for method chaining (will I ever need this?)
        """
        union_headlines = self.headlines.copy()
        union_headlines.update(other.headlines)
        
        for thread_num, headline in other.headlines.iteritems():
            if thread_num in self.headlines:
                # Take the one with greater posts
                other_num_posts = other.headlines[thread_num].num_posts
                this_num_posts = self.headlines[thread_num].num_posts
                if other_num_posts > this_num_posts:
                    self.headlines[thread_num] = other.headlines[thread_num].copy()
            else:
                # New thread
                self.headlines[thread_num] = other.headlines[thread_num].copy()
        
        return self

    def to_board(self):
        """Convert this board state to a full board."""
        board = Board(self.board_iden)
        board.headlines = self.headlines.values()
        board.headlines.sort(key=lambda h: h.sort_key, reverse=True)        
        return board


class BoardStateDiff(object):
    """A diff between two different board states."""
    def __init__(self, board_iden, num_new_posts, num_new_threads):
        self.board_iden = board_iden
        self.num_new_posts = num_new_posts
        self.num_new_threads = num_new_threads
