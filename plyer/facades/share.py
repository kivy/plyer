# coding=utf-8
'''
Share
=====

The :class:`Share` provides access to public methods to share a file or text or ...

.. note::
    In android you need external storage permissions.

.. versionadded:: 2.1.0

This can be used to activate the sharesheet on supported OS.

Simple Examples
---------------

Share text::

    >>> from plyer import share
    >>> share.share_text(text, title)

Share file::

    >>> share.share_file(data, filename, title)

Supported Platforms
-------------------
Android, iOS

'''
from typing import Tuple


class Share:
    """
    Share facade.
    """

    def share_text(self, text: str, title: str,
        size: Tuple[int, int]=(32, 32),
        pos:Tuple[int, int]=(200, 200),
        arrow_direction:int=0):
        """
        Share Sheet for text
        """
        self._share_text(text, title)

    def share_file(
        self, data: str, filename: str, title: str,
        size: Tuple[int, int]=(1, 1),
        pos:Tuple[int, int]=(0, 0),
        arrow_direction:int=0):
        """
        Share a file
        """
        self._share_file(data, filename, title, size, pos, arrow_direction)

    # private

    def _share_text(self, text:str,
        size: Tuple[int, int]=(32, 32),
        pos:Tuple[int, int]=(200, 200),
        arrow_direction:int=0):
        raise NotImplementedError()

    def _share_file(self, data: str, filename: str, titile: str,
        size: Tuple[int, int]=(32, 32),
        pos:Tuple[int, int]=(200, 200),
        arrow_direction:int=0):
        raise NotImplementedError()
