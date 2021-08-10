import pygame
from time import sleep
from tkinter import *
from tkinter import messagebox
import sys

pygame.init()

WIDTH = 600
HEIGHT = WIDTH

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Djistra\'s path finding algorithm')

class Node:
	def __init__(self, x, y, width, height, row, col):
		self.x = x
		self.y = y
		self.width = width 
		self.height = height
		self.row = row
		self.col = col
		self.visited = False
		self.prev_node = None
		self.color = (255,255,255)
		self.neighbours = []
		self.obstacle = False

	def draw_node(self):
		pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))


	def add_neighbours(self, graph):
		if self.row > 0 and self.row < graph.total_rows - 1:
			self.neighbours.append(graph.node_list[self.row + 1][self.col])
			self.neighbours.append(graph.node_list[self.row - 1][self.col])

		if self.col > 0 and self.col < graph.total_rows - 1:
			self.neighbours.append(graph.node_list[self.row][self.col - 1])
			self.neighbours.append(graph.node_list[self.row][self.col + 1])

		if self.row == 0:
			self.neighbours.append(graph.node_list[self.row + 1][self.col])

		if self.row == graph.total_rows - 1:
			self.neighbours.append(graph.node_list[self.row - 1][self.col])

		if self.col == 0:
			self.neighbours.append(graph.node_list[self.row][self.col + 1])

		if self.col == graph.total_rows - 1:
			self.neighbours.append(graph.node_list[self.row][self.col - 1])

class Graph:
	def __init__(self, space_between):
		self.node_list = []
		self.space_between = space_between
		self.total_rows = WIDTH//self.space_between
		self.start_node = None
		self.end_node = None
		self.partially_visited_nodes = [] 
		self.search_started = False
		self.current_node = None
		self.top = -1
		self.over = False
		self.shortest_path = []
		self.shortest_path_length = 0

	def give_connections(self):
		pass

	def initialize_nodes(self):
		for row in range(self.total_rows):
			row_node_list = []
			for col in range(self.total_rows):
				row_node_list.append(Node(col * self.space_between, row * self.space_between, self.space_between, self.space_between, row, col))
			self.node_list.append(row_node_list)

	def draw_lines(self):
		for row in range(self.total_rows):
			pygame.draw.line(screen, (0,0,0), (0, (row+1) * self.space_between) , (WIDTH, (row+1) * self.space_between), 1)
			for col in range(self.total_rows):
				pygame.draw.line(screen, (0,0,0), ((col + 1) * self.space_between,row+1) , ((col+1) * self.space_between, (row+1) * self.space_between))

	def place_node(self):
		for row in self.node_list:
			for node in row:
				node.draw_node()


	def check_for_start(self):
		if self.start_node and self.end_node and not self.search_started:
			self.search_started = True
			self.current_node = self.start_node

	def start_finding(self):
		if self.search_started:
			self.current_node.visited = True
			
			for neighbour in self.current_node.neighbours:
				if not neighbour.visited and neighbour not in self.partially_visited_nodes and not neighbour.obstacle:
					neighbour.prev_node = self.current_node
					self.partially_visited_nodes.append(neighbour)
			self.top +=1
			self.current_node = self.partially_visited_nodes[self.top]
			if self.current_node == self.end_node:
				self.current_node.color = (0,0,255)
				self.add_short_path()
				self.over = True
				self.search_started = False
			else:
				self.current_node.color = (0, 255, 0)

	def add_short_path(self):
		self.current_node = self.current_node.prev_node
		while self.current_node:
			if self.current_node not in self.shortest_path:
				self.shortest_path.append(self.current_node)
				self.current_node = self.current_node.prev_node
		self.shortest_path_length = len(self.shortest_path)


	def mark_short_path(self):
		self.current_node = self.shortest_path.pop()
		if len(self.shortest_path) == self.shortest_path_length - 1:
			self.current_node.color = (255,0,0)
		else:
			self.current_node.color = (255,255,0)


def retry_window():
	root = Tk()
	root.geometry("300x200")
	root.overrideredirect(1)
	root.withdraw()
	choice = messagebox.askokcancel("PATH FOUND!!","DO YOU WISH TO TRY AGAIN?")
	if choice:
		main()
	else:
		pygame.quit()
		sys.exit()
	root.mainloop()

def main():
	clock = pygame.time.Clock()
	running = True
	graph = Graph(20)
	graph.initialize_nodes()
	for row in graph.node_list:
		for node in row:
			node.add_neighbours(graph)

	while running:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if not graph.search_started:
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					col,row = pos[0],pos[1]
					row = row//20
					col = col//20
					node = graph.node_list[row][col]
					if not graph.start_node and not graph.end_node:
						if node != graph.end_node:
							node.color = (255, 0 ,0)
							graph.start_node = node
					elif graph.start_node == node:
						graph.node_list[row][col].color = (255,255,255)
						graph.start_node = None
					elif not graph.end_node:
						if node != graph.start_node:
							node.color = (0,0,255)
							graph.end_node = node
					elif graph.end_node == node:
							graph.node_list[row][col].color = (255,255,255)
							graph.end_node = None
					else:
						if node.obstacle:
							node.obstacle = False
							node.color = (255,255,255)
						else:
							node.color = (0, 0, 0)
							node.obstacle = True


		if graph.over:
			if len(graph.shortest_path) > 0:
				graph.mark_short_path()
			else:
				sleep(2)
				retry_window()

		if not graph.search_started:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE]:
				graph.check_for_start()

		graph.start_finding()

		graph.place_node()
		graph.draw_lines()
		pygame.display.update()

if __name__ == "__main__":
	main()