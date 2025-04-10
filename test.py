def generate_tesseract_vertices():
    vertices = []
    # Генерируем все возможные комбинации координат (0 или 1) для 4-мерного пространства
    for i in range(16):  # 2^4 = 16
        # Формируем координаты в 4D
        vertex = [(i >> j) & 1 for j in range(4)]
        vertices.append(vertex)
    return vertices

# Генерация вершин тессеракта
tesseract_vertices = generate_tesseract_vertices()

# Вывод вершин
for i, vertex in enumerate(tesseract_vertices):
    print(f"Вершина {i + 1}: {vertex}")
