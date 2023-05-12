#!/usr/bin/env python3

from . import engine

storage = engine.file_storage.FileStorage()
storage.reload()
