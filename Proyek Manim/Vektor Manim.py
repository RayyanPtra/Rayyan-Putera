# Nama : Mohammad Rayyan Putera Hindam
# Kelas : D4SM-48-05
# Nim : 707082400011

from manim import *

class VectorOperations(Scene):
    def construct(self):
        # Membuat sumbu x dan y (Membuat sumbu koordinat)
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            axis_config={"color": BLUE},
        )
        # Menambahkan label pada sumbu
        axes_labels = axes.get_axis_labels(x_label='x', y_label='y')

        # Membuat dua vektor
        vector_a = Arrow(ORIGIN, [2, 2, 0], buff=0, color=YELLOW)
        vector_b = Arrow(ORIGIN, [-2, 1, 0], buff=0, color=GREEN)

        # Menambahkan teks untuk vektor
        vector_a_label = Tex("$\\mathbf{a}$").next_to(vector_a, RIGHT)
        vector_b_label = Tex("$\\mathbf{b}$").next_to(vector_b, LEFT)

        # Menambahkan operasi penjumlahan vektor
        sum_vector = Arrow(ORIGIN, [0, 3, 0], buff=0, color=RED)
        sum_label = Tex("$\\mathbf{a} + \\mathbf{b}$").next_to(sum_vector, UP)

        # Menampilkan sumbu dan vektor pertama
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(vector_a), Write(vector_a_label))
        self.play(Create(vector_b), Write(vector_b_label))
        self.wait(1)

        # Menambahkan animasi penjumlahan vektor
        self.play(Transform(vector_a, sum_vector), Transform(vector_a_label, sum_label))
        self.wait(1)

        # Perkalian vektor dengan skalar
        scalar_multiplication = Arrow(ORIGIN, [4, 4, 0], buff=0, color=PURPLE)
        scalar_label = Tex("$2 \\cdot \\mathbf{a}$").next_to(scalar_multiplication, RIGHT)

        # Animasi perkalian skalar
        self.play(Transform(vector_a, scalar_multiplication), Transform(vector_a_label, scalar_label))
        self.wait(1)

        # Menghitung dan menunjukkan hasil perkalian silang (cross product)
        cross_product_vector = Arrow(ORIGIN, [0, 0, 3], buff=0, color=ORANGE)
        cross_product_label = Tex("$\\mathbf{a} \\times \\mathbf{b}$").next_to(cross_product_vector, DOWN)

        # Menampilkan hasil perkalian silang
        self.play(Create(cross_product_vector), Write(cross_product_label))
        self.wait(1)

        # Menghapus semua objek untuk akhir animasi
        self.play(FadeOut(vector_a), FadeOut(vector_b), FadeOut(vector_a_label), FadeOut(vector_b_label), FadeOut(sum_vector), FadeOut(sum_label), FadeOut(scalar_multiplication), FadeOut(scalar_label), FadeOut(cross_product_vector), FadeOut(cross_product_label))
