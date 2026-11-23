import unittest

from painel.core.entidades import Aluno, Nota

class TestAluno(unittest.TestCase):
    def test_calcula_media_aluno(self):
        aluno = Aluno(1030, "Enzo Borges", "3C")
        notas = [
            Nota(1030, "Português", "P2", 8.2),
            Nota(1030, "Português", "P1", 9.3),
            Nota(1016, "Matemática", "P1", 4.8),
] 

        self.assertEqual(aluno.media(notas), 8.75)

    def test_sem_notas(self):
        aluno = Aluno(1030, "Enzo Borges", "3C")

        self.assertIsNone(aluno.media([]))

    def test_situacao_aprovado(self):
        aluno = Aluno(1030, "Enzo Borges", "3C")
        notas = [Nota(1030, "Português", "P1", 8.0)]

        self.assertEqual(aluno.situacao(notas, 6.0, 4.0), "aprovado")

    def test_situacao_recuperacao(self):
            aluno = Aluno(1030, "Enzo Borges", "3C")
            notas = [Nota(1030, "Português", "P1", 5.0)]

            self.assertEqual(aluno.situacao(notas, 6.0, 4.0), "recuperação")

    def test_situacao_reprovado(self):
                aluno = Aluno(1030, "Enzo Borges", "3C")
                notas = [Nota(1030, "Português", "P1", 3.0)]
    
                self.assertEqual(aluno.situacao(notas, 6.0, 4.0), "reprovado")

if __name__=="__main__":
    unittest.main()
