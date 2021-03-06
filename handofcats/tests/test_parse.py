# -*- coding:utf-8 -*-
import unittest


class TestIterateFunction(unittest.TestCase):
    def _getTargetClass(self):
        from handofcats.parsercreator import ArgumentParserCreator
        return ArgumentParserCreator

    def _makeOne(self, fn):
        import inspect
        argspec = inspect.getargspec(fn)
        return self._getTargetClass()(argspec)

    def testiterate_positionals(self):
        def f(x, y, z):
            pass

        target = self._makeOne(f)
        result = list(target.iterate_positionals())
        self.assertEqual(["x", "y", "z"], result)

    def testiterate_positionals2(self):
        def f(x, y, z=None, flag=False, **kwargs):
            pass

        target = self._makeOne(f)
        result = list(target.iterate_positionals())
        self.assertEqual(["x", "y"], result)

    def testiterate_optionals(self):
        def f(a=True, b=None, c=False, **kwargs):
            pass

        target = self._makeOne(f)
        result = list(target.iterate_optionals())
        self.assertEqual([("a", True), ("b", None), ("c", False)], result)

    def testiterate_optionals2(self):
        def f(x, y, z=None, flag=False, **kwargs):
            pass

        target = self._makeOne(f)
        result = list(target.iterate_optionals())
        self.assertEqual([("z", None), ("flag", False)], result)


class TestCreateParser(unittest.TestCase):
    def _getTargetClass(self):
        from handofcats.parsercreator import ArgumentParserCreator
        return ArgumentParserCreator

    def _createOne(self, fn):
        import inspect
        argspec = inspect.getargspec(fn)
        return self._getTargetClass()(argspec)

    def test_create_parser(self):
        def f(config, x, y=None):
            pass

        target = self._createOne(f)
        parser = target.create_parser()

        actual = list(sorted([ac.dest for ac in parser._actions]))
        expected = list(sorted(["config", "x", "y", "help"]))
        self.assertEqual(actual, expected)

    def test_create_parser_skip_options(self):
        def f(config, x, y=None):
            pass

        target = self._createOne(f)
        parser = target.create_parser(skip_options=["config"])

        actual = list(sorted([ac.dest for ac in parser._actions]))
        expected = list(sorted(["x", "y", "help"]))
        self.assertEqual(actual, expected)


class TestGetHelpDict(unittest.TestCase):
    def _callFUT(self, doc):
        from handofcats import get_help_dict
        return get_help_dict(doc)

    def test_it(self):
        doc = """
        this is description message
        hello hello hello

        :param x: x of args
        :param y: y of args
        :rtype: int
        """
        result = self._callFUT(doc)
        expected = {"x": "x of args", "y": "y of args"}
        self.assertEqual(expected, result)

    def test_it_with_type(self):
        doc = """
        this is description message
        :param int x: x of args
        :param str y: y of args
        :rtype: int
        """
        result = self._callFUT(doc)
        expected = {"x": "x of args", "y": "y of args"}
        self.assertEqual(expected, result)


class TestGetDescription(unittest.TestCase):
    def _callFUT(self, doc):
        from handofcats import get_description
        return get_description(doc)

    def test_it(self):
        doc = """
        this is description message
        :param int x: x of args
        :param str y: y of args
        :rtype: int
        """
        result = self._callFUT(doc)
        expected = "this is description message"
        self.assertEqual(expected, result)

    def test_it__long(self):
        doc = """
        this is description message
        hello hello hello
        :param int x: x of args
        :param str y: y of args
        :rtype: int
        """
        result = self._callFUT(doc)
        expected = """this is description message\nhello hello hello"""
        self.assertEqual(expected, result)
