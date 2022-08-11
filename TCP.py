import colorama
colorama.init();
from colorama import Fore, Back, Style #Цвета текста
from tabulate import tabulate #Вывод красивой таблицы
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import itertools
import warnings


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~| Функции |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Функция спрашивает у пользователя все города и связи между ними. Также есть возможность импортировать данные с .txt файла
def create_matrix(file_name=False):
	global matrix, start, cities
	matrix = {}

	def sorting(dictionary):
		return { city: dictionary[city] for city in sorted(dictionary)}

	if not(file_name) or file_name=='':
		#До тех пор, пока человек не введёт ENTER - спрашиваем у него расстояние между городами
		while True:
			try:
				print(f'{Fore.CYAN}[Откуда] [Куда] [Цена проезда]: ', end='')
				from_road, to_road, price = input().split();
				from_road, to_road = from_road[0].title(), to_road[0].title()

				if not(price.replace('.', '').isdigit()):
					print(f'{Fore.RED}Расстояние должно быть числом!{Fore.CYAN}\n'); continue

				else:
					matrix[from_road] = {to_road: float(price)} if from_road not in matrix else matrix[from_road] | {to_road: float(price)}
					matrix[to_road] = {from_road: float(price)} if to_road not in matrix else matrix[to_road] | {from_road: float(price)}
			
			except Exception as error:
				break
	else:
		with open('Примеры/'+file_name.replace('.txt', '')+'.txt', 'r') as file:
			for line in file:
				try:
					from_road, to_road, price = line.split()
					from_road, to_road = from_road[0].title(), to_road[0].title()

					if not(price.replace('.', '').isdigit()):
						print(f'{Fore.RED}Расстояние должно быть числом!{Fore.CYAN}\n'); continue
					else:
						matrix[from_road] = {to_road: float(price)} if from_road not in matrix else matrix[from_road] | {to_road: float(price)}
						matrix[to_road] = {from_road: float(price)} if to_road not in matrix else matrix[to_road] | {from_road: float(price)}
				except Exception as error:
					print(f'Что-то не так со строкой {line.strip()}')

	for city_1 in matrix:
		for city_2 in matrix:
			if city_2 not in matrix[city_1] and city_1 != city_2:
				print(f'\n{Fore.RED}Вы не указали расстояние между пунктами {city_1} и {city_2}: ', end='')
				while True:
					try:
						print(f'\n{Fore.CYAN}Цена из города {city_1} в {city_2}: ',end='')
						price = float(input());
						matrix[city_1] = {city_2: price} if city_1 not in matrix else matrix[city_1] | {city_2: price}
						matrix[city_2] = {city_1: price} if city_2 not in matrix else matrix[city_2] | {city_1: price}
						break

					except Exception as error:
						print(f'{Fore.RED}Расстояние должно быть числом!{Fore.CYAN}\n');

	matrix = { city: sorting(matrix[city]) for city in matrix}; matrix = sorting(matrix)

	result = [[' ']+[ city for city in matrix]]+[ [city_1]+[ '   ~ ' if city_1==city_2 else matrix[city_1][city_2] for city_2 in matrix ] for city_1 in matrix]
	
	while start not in matrix:
		start = input('С какого узла начинать: ').upper();
		if start not in matrix: print('Такого узла нет!')

	cities = list(matrix.keys())
	print(tabulate(result, tablefmt='grid'))


#Функция рисует матрицу на определённой фигуре MatPlotLib
def generate_graph(matrix, ax_object, iterative_way=False, dynamic_way=False):
	
	already_used = []
	Graph = nx.Graph();
	#Циклом связываем друг с другом все матрицы
	for city_1 in matrix:
		for city_2 in matrix:
			if (city_1, city_2) not in already_used and (city_2, city_1) not in already_used and city_1 != city_2:
				try:
					Graph.add_edge(city_1, city_2, weight=matrix[city_1][city_2])
				except Exception as error:
					print(city_1, city_2, matrix[city_1][city_2])

	#Берём координаты каждого созданного узла на графике
	pos = nx.spring_layout(Graph, seed=7)

	#Рисуем узлы графа
	nodes = nx.draw_networkx_nodes(Graph, pos, ax=ax_object, node_size=500, node_color='white')
	nodes.set_edgecolor('r')
	nx.draw_networkx_edges(Graph, pos, ax=ax_object, width=4)
	if iterative_way:
		iterative_way, length = iterative_way[0].split(' -> '), iterative_way[1]
		edge_list = [ (iterative_way[i], iterative_way[i+1]) for i in range(len(iterative_way)-1) ]
		nx.draw_networkx_edges(Graph, pos, ax=ax_object, width=2.5, edge_color='cyan', edgelist=edge_list)
		axes[1].set_title(f'Переборное решение ≈ {length}км\nПуть: {" --- ".join(iterative_way)}', pad=10) #<--- Заголовок первого графика
		axes[1].plot()

	if dynamic_way:
		edge_list = [ (dynamic_way[i], dynamic_way[i+1]) for i in range(len(dynamic_way)-1) ]
		nx.draw_networkx_edges(Graph, pos, ax=ax_object, width=2.5, edge_color='yellow', edgelist=edge_list)
		length = sum([ matrix[dynamic_way[i]][dynamic_way[i+1]] for i in range(len(dynamic_way)-1) ])
		axes[2].set_title(f'Динамическое решение ≈ {length}км\nПуть: {" --- ".join(dynamic_way)}', pad=10) #<--- Заголовок первого графика
		print(f'Решение методом динамического программирования\n{"-->".join(dynamic_way)} ≈ {length}')

	#Рисуем подписи к узлам
	nx.draw_networkx_labels(Graph, pos, ax=ax_object, font_size=15, font_color='red')

	#Рисуем подписи к рёбрам узлов
	edge_labels = nx.get_edge_attributes(Graph, "weight")
	nx.draw_networkx_edge_labels(Graph, pos, edge_labels, ax=ax_object, font_size=10, font_color='red', font_weight='bold')
	ax_object.grid()

def iterative_method():
	global iterative_matrix
	print(f'\nРешение методом перебора: ')
	min_way = ['', 10**10];
	for way in itertools.permutations(matrix.keys()):
		way = list(way)+[start]
		if way[0] == start:
			current_way_length = sum(list([ matrix[way[i]][way[i+1]] for i in range(len(way)-1) ]))
			if current_way_length < min_way[1]:
				min_way[0], min_way[1] = " -> ".join(way), current_way_length
				print(f' {min_way[0]} ≈ {min_way[1]}')
	return min_way

def dynamic_method(massiv, i):
	if len(massiv) == 1:
		return massiv[0]

	most_profitable = [None, 10**10]
	for city in massiv:
		if i != city:
			if matrix[i][city] < most_profitable[1]:
				most_profitable[0], most_profitable[1] = city, matrix[i][city]

	massiv.remove(i)
	if i == start:
		return i+most_profitable[0]+dynamic_method( massiv, most_profitable[0] )
	else:
		return most_profitable[0]+dynamic_method( massiv, most_profitable[0] )


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~| Переменные |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
matrix = {};
dynamic_solution = [];
iterative_solution = [];
start = None;


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~| Запуск программы |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
matplotlib.use('Qt5Agg') #<--- Устанавливает бэкенд вывода, они бывают:


create_matrix(input('Название файла: ')) #<--- Спрашиваем у пользователя города, создаём матрицу
iterative_solution = iterative_method() #<--- Находим переборное решение
dynamic_solution = list(dynamic_method(list(matrix.keys()), start)[:-1]+start);
figure, axes = plt.subplots(1, 3); #<--- Создаём три фигуры: для основного графика, переборного и динамического
axes[1].set_xlabel('Проект Рамазана Ойболатова', fontsize='large')
figure.set_facecolor('#c4ddff') #<--- Установка заднего фона
figure.set_figheight(8) #<--- Устанавливаем ширину и высоту изначального окна
figure.set_figwidth(15)
axes[0].set_title('Оригинальный график', pad=10) #<--- Заголовок первого графика
axes[1].set_title('Переборное решение ≈ None`', pad=10) #<--- Заголовок второго графика
axes[2].set_title('Динамическое решение ≈ None', pad=10) #<--- Заголовок третьего графика


generate_graph( matrix, axes[0] ) #<--- Генерируем оригинальный граф со всеми городами
generate_graph( matrix, axes[1], iterative_way=iterative_solution ) #<--- Переборное решение
generate_graph( matrix, axes[2], dynamic_way=dynamic_solution ) #<--- Динамическое решение

plt.show()
