#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from enum import Enum

import pygame
import math

from pygame.event import Event
from pygame import Vector2
from game_callback import GameCallback
from scene import Scene


from camera import Camera
from item import CompositeItem, Item, ImageItem

from asyncio import Event

import pygame
from pygame import Vector2

from camera import Camera
from game_callback import GameCallback
from item import ImageItem, CompositeItem
from scene import Scene

import random

from player import Player
from utils import Road, Protein


class SceneQuentin(Scene):
    def __init__(self,  game_callback: GameCallback, screen: pygame.Surface):
        #copy from SceneTest
        super().__init__(game_callback, screen)
        self._camera = Camera(self._screen)

        # item image background
        self._camera_background = Camera(self._screen);
        self._image_background = ImageItem(self._camera_background, Vector2(0, 0), Vector2(1, 9/16), image='background.png')
        self._add_item(self._image_background)

        # defining roads y position
        road_y_1 = 0.0
        road_y_2 = 0.2

        # item image composite roads
        self._road1 = Road(self._camera, Vector2(0, road_y_1))
        self._road1.set_z_value(20)
        self._add_item(self._road1)

        self._road2 = Road(self._camera, Vector2(0, road_y_2))
        self._road2.set_z_value(20)
        self._add_item(self._road2)

        # roads
        self._player1 = Player(self._camera, Vector2(0, road_y_1 - 0.1))
        self._player1.set_z_value(30)
        self._add_item(self._player1)

        self._player2 = Player(self._camera, Vector2(0, road_y_2 - 0.1))
        self._player2.set_z_value(30)
        self._add_item(self._player2)

        # proteins
        self._proteins1 = []
        self._proteins2 = []

        # setting the road for both player
        prot_delta = -0.02

        for protein_list, road_y in zip([self._proteins1, self._proteins2], [road_y_1, road_y_2]):
            protein_list.append(Protein(self._camera, Vector2(0, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(0.3, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(0.7, road_y + prot_delta)))
            protein_list.append(Protein(self._camera, Vector2(1, road_y + prot_delta)))

        for protein in self._proteins1 + self._proteins2:
            self._add_item(protein)

    def manage_events(self, event: Event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self._player1.set_right(True)
                elif event.key == pygame.K_LEFT:
                    self._player1.set_left(True)
                elif event.key == pygame.K_UP:
                    self._player1.set_up(True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self._player1.set_right(False)
                elif event.key == pygame.K_LEFT:
                    self._player1.set_left(False)
                elif event.key == pygame.K_UP:
                    self._player1.set_up(False)

    def _update_cameras(self):
        camera_pos = Vector2(0.5 * self._player1.pos.x + 0.5 * self._player2.pos.x + 0.1/self._camera.zoom, 0)
        self._camera.set_pos(camera_pos)

        if abs((self._camera.pos - self._player1.pos).length()) > 0.3 / self._camera.zoom:
            self._camera.dzoom(-0.02)

        self._camera_background.set_pos(0.1 * (self._camera.pos / self._screen.get_width()))

    def update(self):
        self._update_cameras()
        super().update()
        for protein in self._proteins1:
            if self._player1.rect.colliderect(protein.rect):
                self._remove_item(protein)
                self._proteins1.remove(protein)

        for protein in self._proteins2:
            if self._player2.rect.colliderect(protein.rect):
                self._remove_item(protein)
                self._proteins2.remove(protein)
