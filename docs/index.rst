.. Play Smarter documentation master file, created by
   sphinx-quickstart on Sun Jan 31 17:17:30 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Play Smarter's documentation!
========================================

Contents:

.. toctree::
   :maxdepth: 2

# Mock

Mock is not a built-in library in python 2.7. It is included in 3.3 by default. It allows you to test the some of the functions or classes without actually running the real ones. This can come handy when actually calling the 'real' functions will cause side-effects.

For example, you don't want your disk tray to jump out every time you test its behavior. Or, you definitely don't want to post something to Facebook when you are testing Facebook sharing. By mocking those parts, i.e., by substituting those functions with some fake functions that you cook up to simulate the behaviors. You could be sure that your code are working without causing any trouble.

## Mock and MagicMock
Mock and MagicMock objects create all attributes and methods as you access them and store details of how they have been used.

### side_effect
When you pass an iterable to side_effect, you should expect the mock to yield a value for you whenever you call it.
```
>>> mock = Mock()
>>> mock.side_effect = [3, 2, 1]
>>> mock(), mock(), mock()
(3, 2, 1)
```

also, `side_effect` is called with the same arguments as the mock.
```
>>> def side_effect(value):
...     return value + 1
...
>>> m = MagicMock(side_effect=side_effect)
>>> m(1)
2
>>> m(2)
3
>>> m.mock_calls
[call(1), call(2)]
```

## patch()
First thing first, patch will return a mock object. Depending on the passed arguments, the return object can either be a simple Mock object or a MagicMock object.
The patch decorator makes it easy to mock classes or objects in a module under test.

### How to properly use patch
If `patch` is used as a decorator and **new** is omitted, the created mock is passed in as an extra aurgument to the decorated function.

Suppose now we have a module called **mymodule** that can remove file:
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def rm(filename):
    os.remove(filename)
```

Now we would like to test it using mock:
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mymodule import rm

import mock
import unittest

class RmTestCase(unittest.TestCase):

    @mock.patch('mymodule.os')
    def test_rm(self, mock_os):
        rm("any path")
        # test that rm called os.remove with the right parameters
        mock_os.remove.assert_called_with("any path")
```
Pay attention that we are mocking `mymodule.os` instead of `os`.
> Mock an item where it is used, not where it came from.
Why? Because Python will create an `os` module for `mymodule` during runtime in its local scope.

Another thing to notice is that Mock will create all attributes and methods as you access them and **store details of how they have been used**. What that means is that you can use `assert_called_with` to test whether the function is called with the arguments that you have in your mind.

### How to mock a function
This is quite common and can be easily explained with the following code.
Say we create a module whose name is called **fots**:
```
from os import urandom


def abc_urandom(length):
    return 'abc' + urandom(length)
```
Then we can mock the urandom function in the fots module like this:
```
import unittest
import mock

from fots import abc_urandom


class TestRandom(unittest.TestCase):
    @mock.patch('fots.urandom', side_effect=simple_urandom)
    def test_abc_urandom(self, abc_urandom_function):
        assert abc_urandom(5) == 'abcfffff'
```

Or if you just want to mock the return value, you could do this:
`@mock.patch('os.urandom', return_value='pumpkins')`


### Sequence matters
Notice the sequence. The decorated functions are applied from the bottom up.
```
>>> from unittest.mock import patch
>>> @patch('module.ClassName2')
... @patch('module.ClassName1')
... def test(MockClass1, MockClass2):
...     module.ClassName1()
...     module.ClassName2()
...     assert MockClass1 is module.ClassName1
...     assert MockClass2 is module.ClassName2
...     assert MockClass1.called
...     assert MockClass2.called
...
>>> test()
```

## The usage

## Reference
[Official doc](https://docs.python.org/3/library/unittest.mock.html)
[Mocking in Python: A Guide to Better Unit Tests | Toptal](http://www.toptal.com/python/an-introduction-to-mocking-in-python)
[Mock function](http://fgimian.github.io/blog/2014/04/10/using-the-python-mock-library-to-fake-regular-functions-during-tests/)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

