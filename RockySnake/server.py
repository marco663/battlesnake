import os
import random
import cherrypy
import pandas as pd

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#E80978",  # TODO: Personalize
            "head": "shac-tiger-king",  # TODO: Personalize
            "tail": "shac-mouse",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        
        valid_moves = self.get_valid_moves(data)
        move = random.choice(valid_moves)

        print(f"MOVE: {move}")

        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"

    def get_valid_moves(self, data):

      head_loc = data["you"]["head"]
      moves = ["up", "down", "left", "right"]
      board_width = data["board"]["width"]
      board_height = data["board"]["height"]

      x = head_loc["x"]
      y = head_loc["y"]

      if x == 0:
        moves.remove("left")
      elif x == (board_width - 1):
        moves.remove("right")
      if y == 0:
        moves.remove("down")
      elif y == (board_height - 1):
        moves.remove("up")

      # From the possible moves, remove those that will hit the body part
      removes = []
      for x in moves:
        res = self.is_body_hitted(x, head_loc, data)
        if res[0]:
          removes.append(x)

      for x in removes:
        moves.remove(x)
        
      return moves


    def is_body_hitted(self, move, head_loc, data):
      
      x = head_loc["x"]
      y = head_loc["y"]
      
      if move == "left":
        x -= 1
      elif move == "right":
        x += 1
      elif move == "down":
        y -= 1
      else:
        y += 1
      
      new_head_loc = {"x": x, "y": y}

      for body_part in data["you"]["body"]:
        if new_head_loc["x"] == body_part["x"] and new_head_loc["y"] == body_part["y"]:
          return [True, new_head_loc]
      return [False, new_head_loc]


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
