import unittest
import testes


def executar():
    suite = unittest.defaultTestLoader.loadTestsFromModule(
        testes
    )

    resultado = unittest.TextTestRunner(
        verbosity=2
    ).run(suite)

    total = resultado.testsRun
    falhas = len(resultado.failures)
    erros = len(resultado.errors)
    ignorados = len(resultado.skipped)

    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)

    print(f"Testes executados: {total}")
    print(f"Falhas:            {falhas}")
    print(f"Erros:             {erros}")
    print(f"Ignorados:         {ignorados}")

    if falhas == 0 and erros == 0:
        print("\nResultado: TESTES CONCLUÍDOS SEM FALHAS.")
    else:
        print("\nResultado: EXISTEM TESTES COM FALHA OU ERRO.")

    return resultado


if __name__ == "__main__":
    executar()