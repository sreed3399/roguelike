from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING
import random

import color
import exceptions
#from pygame import mixer
from load_resources import sounds
import os


#import mapreader

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


#loadActionSounds()


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def energy(self) -> int:
        return self.entity.energy

    @property
    def name(self) -> int:
        return self.entity.name

    @property
    def speed(self) -> int:
        return self.entity.speed

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine


    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                self.entity.energy -= 500
                return

        raise exceptions.Impossible("There is nothing here to pick up.")

class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)
            self.entity.energy -= 1000



#class EscapeAction(Action):
#    def perform(self) -> None:
#        raise SystemExit()

class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)
            
        self.entity.inventory.drop(self.item)
        self.entity.energy -= 500

class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)
        self.entity.energy -= 1000

class WaitAction(Action):
    def perform(self) -> None:
        self.entity.energy -= 1000
        pass


class TakeStairsDownAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        #print(self.engine.game_map.downstairs_location)
        #print(self.entity.x, self.entity.y)

        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            SaveMapAction(self.entity)
            
            #self.engine.game_world.move_floor()
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "You descend the staircase.", color.descend
            
            )
        else:
            raise exceptions.Impossible("There is no way down here.")

class TakeStairsUpAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        #print(self.engine.game_map.upstairs_location)
        #print(self.entity.x, self.entity.y)
        if (self.entity.x, self.entity.y) == self.engine.game_map.upstairs_location:

            
            #self.engine.game_map.save_map()

            #self.engine.game_world.move_floor()
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "You ascend the staircase.", color.descend
            
            )
        else:
            raise exceptions.Impossible("There is no way up here.")


class SaveMapAction(Action): # Save action items added by steve
    def perform(self) -> None:
        
        
        print(self.engine.game_map.entities)

        path = "saves/"+self.name
        if not os.path.exists(path):
            os.mkdir(path)
        #self.engine.game_map.save_map(path)
        self.engine.game_map.save_map(path)
        


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy
    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)
    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    
    def perform(self) -> None:
        raise NotImplementedError()

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        
        target = self.target_actor
        
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        
        if random.randint(1,20 + self.entity.toHit) >= target.dv:         
            
            #time.sleep(.1)

            sounds.playSound("hit")
            #hit.play()
            if damage > 0:
                print(f"{attack_desc} for {damage} hit points.")
                self.engine.message_log.add_message(
                    f"{attack_desc} for {damage} hit points.", attack_color
                )
                target.fighter.hp -= damage
            else:
                print(f"{attack_desc} but does no damage.")
                self.engine.message_log.add_message(
                    f"{attack_desc} but does no damage.", attack_color
                )
        else:
            print(f"{attack_desc} but misses!")
            self.engine.message_log.add_message(
                f"{attack_desc} but misses!", attack_color)
            sounds.playSound("miss")


        self.entity.energy -= 1000


class MovementAction(ActionWithDirection):

    def perform(self) -> None:
        
               
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")       

        self.entity.move(self.dx, self.dy)
        self.entity.energy -= 1000
        #print(self.entity.name, self.entity.energy,self.entity.fighter.energy)
        #print(self.name,self.energy)

