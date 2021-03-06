INSERT INTO recipe_requirement(recipe_id, ingredient_id, required_amount)
VALUES
    (1, 1, 1), (1, 2, 0.25), (1, 3, 0.25), (1, 4, 1), (1, 5, 1), (1, 6, 0.33),
    (2, 7, 3), (2, 8, 1), (2, 9, 1),
    (3, 10, 10),
    (4, 2, 0.25), (4, 11, 0.25), (4, 12, 2), (4, 13, 1), (4, 14, 1), (4, 15, 1), (4, 16, 1), (4, 17, 1),
    (5, 18, 1.5), (5, 19, 5), (5, 20, 3), (5, 21, 2), (5, 22, 0.25), (5, 23, 0.25),
    (6, 24, 1), (6, 21, 2), (6, 25, 2), (6, 22, 1), (6, 7, 1), (6, 26, 1), (6, 27, 2),
    (7, 28, 2), (7, 22, 1), (7, 29, 3), (7, 15, 3), (7, 30, 3),
    (8, 31, 1), (8, 32, 1), (8, 33, 0.75), (8, 15, 2), (8, 34, 0.5), (8, 26, 0.5), (8, 35, 2),
    (9, 26, 0.5), (9, 7, 3), (9, 27, 3), (9, 37, 1), (9, 38, 1.5), (9, 39, 1.5), (9, 22, 0.5), (9, 40, 4), (9, 41, 2),
    (10, 42, 1), (10, 43, 1), (10, 44, 3), (10, 45, 0.5), (10, 46, 1), (10, 32, 1), (10, 20, 0.25), (10, 21, 3), (10, 22, 2), (10, 23, 2),
    (11, 47, 1), (11, 7, 3), (11, 48, 2), (11, 22, 3), (11, 23, 2), (11, 20, 0.5), (11, 27, 1),
    (12, 49, 2), (12, 26, 1.5), (12, 21, 1.5), (12, 50, 3),
    (13, 27, 2), (13, 15, 6), (13, 32, 1), (13, 43, 0.25), (13, 1, 1), (13, 51, 1), (13, 21, 2), (13, 52, 0.4), (13, 53, 0.25), (13, 45, 1.5),
    (14, 54, 1.5), (14, 29, 5), (14, 21, 5), (14, 55, 4), (14, 56, 1), (14, 57, 1), (14, 48, 2), (14, 7, 3),
    (15, 24, 0.5), (15, 20, 0.5), (15, 22, 1), (15, 23, 1), (15, 59, 2), (15, 60, 1), (15, 7, 1), (15, 27, 2),
    (16, 61, 2), (16, 62, 0.25), (16, 63, 4),
    (17, 40, 4), (17, 32, 1), (17, 15, 2), (17, 64, 5), (17, 36, 0.25), (17, 65, 1), (17, 19, 2), (17, 66, 0.25), (17, 22, 1), (17, 23, 1), (17, 7, 2),
    (18, 67, 50), (18, 43, 1), (18, 32, 2), (18, 68, 2), (18, 20, 0.5), (18, 23, 0.5), (18, 69, 0.5), (18, 22, 1.5), (18, 7, 2),
    (19, 70, 4), (19, 22, 1), (19, 23, 1), (19, 24, 0.5), (19, 7, 2), (19, 60, 1),
    (20, 31, 4), (20, 20, 1), (20, 22, 0.5), (20, 71, 8), (20, 4, 2), (20, 5, 1), (20, 72, 0.5), (20, 73, 10), (20, 2, 0.5), (20, 74, 0.5),
    (21, 47, 4), (21, 19, 8), (21, 75, 4), (21, 15, 5), (21, 21, 0.5), (21, 22, 0.25), (21, 76, 1),
    (22, 43, 1), (22, 36, 0.25), (22, 37, 0.5), (22, 68, 1), (22, 33, 0.15), (22, 7, 1), (22, 77, 1.5), (22, 23, 0.5), (22, 22, 2), (22, 78, 6),
    (23, 21, 2), (23, 79, 2), (23, 80, 2), (23, 50, 3), (23, 26, 1),
    (24, 21, 8), (24, 81, 12), (24, 22, 1), (24, 29, 8), (24, 7, 1), (24, 57, 1), (24, 24, 1.25), (24, 82, 0.5), (24, 26, 1), (24, 83, 4),
    (25, 40, 1), (25, 85, 5), (25, 22, 2), (25, 84, 0.25),
    (26, 59, 1), (26, 85, 4), (26, 27, 2), (26, 15, 4), (26, 32, 1), (26, 52, 0.25), (26, 87, 2), (26, 53, 0.25), (26, 86, 1),
    (27, 88, 2), (27, 89, 1.5), (27, 90, 2), (27, 21, 4), (27, 53, 0.125), (27, 91, 0.33),
    (28, 92, 3), (28, 93, 1), (28, 94, 3), (28, 57, 3), (28, 85, 3),
    (29, 95, 1), (29, 37, 0.5), (29, 15, 2), (29, 31, 2), (29, 26, 1.25), (29, 16, 0.125), (29, 96, 3), (29, 22, 2),
    (30, 27, 2), (30, 15, 4), (30, 97, 1), (30, 32, 1), (30, 98,0.25), (30, 99, 2), (30, 100, 2), (30, 101, 0.25), (30, 87, 1);