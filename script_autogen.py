from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww.linkedin.com%2Ffeed%2F")
    page.get_by_placeholder(" ").fill("gabriellbraga2011@gmail.com")
    page.get_by_label("Senha").click()
    page.get_by_label("Senha").press("CapsLock")
    page.get_by_label("Senha").fill("A")
    page.get_by_label("Senha").press("CapsLock")
    page.get_by_label("Senha").fill("Adriana@10")
    page.get_by_label("Entrar", exact=True).click()
    page.goto("https://www.linkedin.com/mynetwork?skipRedirect=true&lipi=urn%3Ali%3Apage%3Ad_flagship3_job_home%3BR%2F4nqO8gSpGSrU3sy1CO9g%3D%3D")
    page.goto("https://www.linkedin.com/mynetwork/grow/")
    page.goto("https://www.linkedin.com/jobs/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people%3Bgvc34c3xRTqsmV328jJDqQ%3D%3D")
    page.goto("https://www.linkedin.com/jobs/")
    page.get_by_role("combobox", name="Pesquisar cargo, competência").click()
    page.get_by_role("combobox", name="Pesquisar cargo, competência").fill("python jr")
    page.get_by_role("combobox", name="Pesquisar cargo, competência").press("Enter")
    page.get_by_label("Avançar para próxima etapa").click()
    page.get_by_label("Selecionado").click()
    page.get_by_label("Avançar para próxima etapa").click()
    page.get_by_label("Possui conhecimento em").select_option("Yes")
    page.get_by_label("Revise sua candidatura").click()
    page.get_by_label("Enviar candidatura").click()
    page.goto("https://www.linkedin.com/jobs/search/post-apply/default/?currentJobId=4261961630&geoId=106057199&keywords=python%20jr&origin=JOBS_HOME_SEARCH_BUTTON&postApplyJobId=4261961630&refresh=true")
    page.get_by_role("button", name="Concluído").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
