class Article:
    all = []

    def __init__(self, author, magazine, title):
        self._author = None
        self._magazine = None
        self._title = None

        self.author = author
        self.magazine = magazine
        self._set_title(title)

        Article.all.append(self)

    # TITLE 
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Immutable after initialization
        pass

    def _set_title(self, value):
        if isinstance(value, str) and 5 <= len(value) <= 50:
            if self._title is None:
                self._title = value

    #AUTHOR
    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        from classes.many_to_many import Author
        if isinstance(value, Author):
            self._author = value

    #MAGAZINE
    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        from classes.many_to_many import Magazine
        if isinstance(value, Magazine):
            self._magazine = value


#AUTHOR


class Author:
    def __init__(self, name):
        self._name = None
        self._set_name(name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Cannot be changed
        pass

    def _set_name(self, value):
        if isinstance(value, str) and len(value) > 0:
            if self._name is None:
                self._name = value

    # ------------ RELATION METHODS ------------
    def articles(self):
        from classes.many_to_many import Article
        return [a for a in Article.all if a.author is self]

    def magazines(self):
        return list({a.magazine for a in self.articles()})

    def add_article(self, magazine, title):
        from classes.many_to_many import Article
        return Article(self, magazine, title)

    def topic_areas(self):
        mags = self.magazines()
        if len(mags) == 0:
            return None
        return list({m.category for m in mags})


#MAGAZINE
class Magazine:
    all = []

    def __init__(self, name, category):
        self._name = None
        self._category = None

        self.name = name
        self.category = category

        Magazine.all.append(self)

    # NAME 
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value

    # CATEGORY 
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value

    #RELATION METHODS
    def articles(self):
        from classes.many_to_many import Article
        return [a for a in Article.all if a.magazine is self]

    def contributors(self):
        return list({a.author for a in self.articles()})

    def article_titles(self):
        arts = self.articles()
        if len(arts) == 0:
            return None
        return [a.title for a in arts]

    def contributing_authors(self):
        arts = self.articles()
        if len(arts) == 0:
            return None

        counts = {}
        for a in arts:
            counts[a.author] = counts.get(a.author, 0) + 1

        result = [auth for auth, count in counts.items() if count > 2]
        return result if result else None

    # BONUS 
    @classmethod
    def top_publisher(cls):
        from classes.many_to_many import Article
        if len(Article.all) == 0:
            return None
        return max(cls.all, key=lambda m: len(m.articles()))
