
"""Pruebas automatizadas para los endpoints y la skill de SkillAPI."""

import unittest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoint(unittest.TestCase):
    def test_health_responde_correctamente(self):
        response = client.get("/api/v1/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_raiz_incluye_documentacion(self):
        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["docs"], "/docs")


class TestSkillsEndpoint(unittest.TestCase):
    def test_lista_la_skill_personalizada(self):
        response = client.get("/api/v1/skills")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text-analysis", response.json()["skills"])


class TestAnalysisEndpoint(unittest.TestCase):
    def test_analisis_completo(self):
        response = client.post(
            "/api/v1/analyze",
            json={
                "text": (
                    "El proyecto es excelente. "
                    "El resultado presenta un problema."
                ),
                "operation": "full",
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["skill_used"], "text-analysis")
        self.assertGreater(data["word_count"], 0)
        self.assertGreater(data["character_count"], 0)
        self.assertIn(
            data["sentiment"],
            ["positivo", "negativo", "neutral"],
        )
        self.assertIsInstance(data["keywords"], list)

    def test_operacion_de_palabras_clave(self):
        response = client.post(
            "/api/v1/analyze",
            json={
                "text": "Python facilita el desarrollo de aplicaciones.",
                "operation": "keywords",
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["sentiment"], "no_calculado")
        self.assertEqual(data["summary"], "")
        self.assertGreater(len(data["keywords"]), 0)

    def test_rechaza_texto_vacio(self):
        response = client.post(
            "/api/v1/analyze",
            json={
                "text": "",
                "operation": "full",
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_rechaza_operacion_no_permitida(self):
        response = client.post(
            "/api/v1/analyze",
            json={
                "text": "Texto de prueba.",
                "operation": "traducir",
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_rechaza_solicitud_sin_texto(self):
        response = client.post(
            "/api/v1/analyze",
            json={"operation": "full"},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main(verbosity=2)
