"""Minimal prototype of a 3D python hunting game using Panda3D.

This script sets up a simple environment with placeholder models for the
python and prey. Arrow keys control the python. The game loop checks for
collisions with prey and respawns prey when eaten.

The implementation is intentionally lightweight and serves as a starting
point for a more graphically rich experience.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import uniform
from typing import List

from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, CollisionNode, CollisionSphere, DirectionalLight
from panda3d.core import NodePath, Vec3, Vec4, CollisionTraverser, CollisionHandlerQueue
from direct.task import Task


@dataclass
class Prey:
    """Simple container for prey nodes and their collision spheres."""

    node: NodePath
    collider: NodePath


class PythonHunter(ShowBase):
    """Main application class."""

    def __init__(self) -> None:
        super().__init__()
        self.cTrav = CollisionTraverser()
        self.collisionHandlerQueue = CollisionHandlerQueue()

        self.disableMouse()
        self.camera.setPos(0, -60, 20)
        self.camera.lookAt(0, 0, 0)

        self._setup_lighting()
        self.python = self._create_python()
        self.prey: List[Prey] = []
        for _ in range(5):
            self.prey.append(self._spawn_prey())

        self.accept("arrow_up", self._move_forward)
        self.accept("arrow_left", self._turn_left)
        self.accept("arrow_right", self._turn_right)

        self.taskMgr.add(self._update, "update")

    # -- Setup helpers -------------------------------------------------
    def _setup_lighting(self) -> None:
        ambient = AmbientLight("ambient")
        ambient.setColor(Vec4(0.4, 0.4, 0.4, 1))
        directional = DirectionalLight("sun")
        directional.setColor(Vec4(0.9, 0.9, 0.8, 1))
        directional.setDirection(Vec3(-1, -1, -2))
        render.setLight(render.attachNewNode(ambient))
        render.setLight(render.attachNewNode(directional))

    def _create_python(self) -> Actor:
        model = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        model.setScale(0.5)
        model.reparentTo(render)
        model.loop("walk")

        # Collision for python
        collider = model.attachNewNode(CollisionNode("python"))
        collider.node().addSolid(CollisionSphere(0, 0, 0, 1))
        self.cTrav.addCollider(collider, self.collisionHandlerQueue)

        return model

    def _spawn_prey(self) -> Prey:
        model = loader.loadModel("models/box")
        model.reparentTo(render)
        model.setScale(0.5, 0.5, 0.5)
        model.setPos(uniform(-20, 20), uniform(-20, 20), 0)

        collider = model.attachNewNode(CollisionNode("prey"))
        collider.node().addSolid(CollisionSphere(0, 0, 0, 0.5))
        self.cTrav.addCollider(collider, self.collisionHandlerQueue)

        return Prey(model, collider)

    # -- Control callbacks --------------------------------------------
    def _move_forward(self) -> None:
        heading = self.python.getHpr().x
        direction = Vec3(0, 1, 0)
        direction.rotateZ(-heading)
        self.python.setPos(self.python, direction * 0.5)

    def _turn_left(self) -> None:
        self.python.setH(self.python.getH() + 5)

    def _turn_right(self) -> None:
        self.python.setH(self.python.getH() - 5)

    # -- Game loop -----------------------------------------------------
    def _update(self, task: Task) -> int:
        for prey in list(self.prey):
            if self.python.getDistance(prey.node) < 1.0:
                prey.node.removeNode()
                self.prey.remove(prey)
                self.prey.append(self._spawn_prey())
        return Task.cont


def main() -> None:
    PythonHunter().run()


if __name__ == "__main__":
    main()
