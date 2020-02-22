#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from enum import Enum


class SceneId(Enum):
    TEST = 0


class GameCallback:
    def set_scene_id(self, scene_id: SceneId):
        raise NotImplementedError