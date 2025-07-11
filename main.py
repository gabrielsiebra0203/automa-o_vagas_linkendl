import asyncio
import time
import random
from playwright.async_api import async_playwright
import json
import os
from typing import List, Dict, Optional

class LinkedInAutomation:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser = None
        self.page = None
        self.credentials = self.load_credentials()
        
    def load_credentials(self) -> Dict[str, str]:
        """Carrega credenciais do arquivo config.json"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Arquivo config.json não encontrado. Criando template...")
            self.create_config_template()
            return {}
    
    def create_config_template(self):
        """Cria template do arquivo de configuração"""
        config = {
            "email": "seu_email@exemplo.com",
            "password": "sua_senha",
            "keywords": ["python", "developer", "desenvolvedor"],
            "locations": ["São Paulo", "Rio de Janeiro", "Remoto"],
            "max_applications": 10,
            "delay_between_actions": [2, 5]
        }
        
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print("Arquivo config.json criado. Configure suas credenciais antes de executar.")
    
    async def start_browser(self):
        """Inicia o navegador Playwright"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
        )
        self.page = await self.browser.new_page()
        
        # Configurar user agent para parecer mais humano
        await self.page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Configurar viewport
        await self.page.set_viewport_size({"width": 1920, "height": 1080})
    
    async def login_linkedin(self) -> bool:
        """Faz login no LinkedIn"""
        try:
            print("🔄 Fazendo login no LinkedIn...")
            
            await self.page.goto('https://www.linkedin.com/login')
            await self.random_delay()
            
            # Preencher email
            await self.page.fill('#username', self.credentials['email'])
            await self.random_delay()
            
            # Preencher senha
            await self.page.fill('#password', self.credentials['password'])
            await self.random_delay()
            
            # Clicar no botão de login
            await self.page.click('button[type="submit"]')
            await self.random_delay(3, 7)
            
            # Novo: aguarda o menu 'Vagas' aparecer
            try:
                await self.page.wait_for_selector('a.global-nav__primary-link[href*="/jobs/"]', timeout=15000)
                print("✅ Login realizado com sucesso!")
                return True
            except Exception:
                print("❌ Falha no login. Menu 'Vagas' não encontrado.")
                return False
                
        except Exception as e:
            print(f"❌ Erro durante o login: {e}")
            return False
    
    async def navigate_to_jobs(self):
        """Navega para a seção de vagas"""
        try:
            print("🔄 Navegando para a seção de vagas...")
            
            # Ir para a página de vagas
            await self.page.goto('https://www.linkedin.com/jobs/')
            await self.random_delay()
            
            print("✅ Página de vagas carregada!")
            
        except Exception as e:
            print(f"❌ Erro ao navegar para vagas: {e}")
    
    async def search_jobs(self, keyword: str, location: str = ""):
        """Busca vagas com os critérios especificados usando seletores mais robustos"""
        try:
            print(f"🔍 Buscando vagas para: {keyword} em {location}")
            # Espera o campo de busca de cargo aparecer (combobox)
            await self.page.wait_for_selector('input[role="combobox"]', timeout=20000)
            cargo_inputs = await self.page.query_selector_all('input[role="combobox"]')
            if cargo_inputs:
                await cargo_inputs[0].click()
                await cargo_inputs[0].fill(keyword)
                await cargo_inputs[0].press('Enter')
                await self.random_delay(2, 4)
            else:
                print("❌ Campo de busca de cargo não encontrado!")
                return
            # Se houver campo de localização, preencha
            if location:
                try:
                    location_inputs = await self.page.query_selector_all('input[role="combobox"]')
                    if len(location_inputs) > 1:
                        await location_inputs[1].click()
                        await location_inputs[1].fill(location)
                        await location_inputs[1].press('Enter')
                        await self.random_delay(2, 4)
                except Exception as e:
                    print(f"⚠️ Não foi possível preencher localização: {e}")
            # Clicar no botão de busca se existir
            try:
                search_buttons = await self.page.query_selector_all('button[aria-label*="Pesquisar"]')
                if search_buttons:
                    await search_buttons[0].click()
                    await self.random_delay(3, 6)
            except Exception as e:
                print(f"⚠️ Não foi possível clicar no botão de busca: {e}")
            print("✅ Busca realizada com sucesso!")
        except Exception as e:
            print(f"❌ Erro na busca de vagas: {e}")
    
    async def filter_easy_apply_jobs(self):
        """Filtra vagas com candidatura simplificada"""
        try:
            print("🔍 Filtrando vagas com candidatura simplificada...")
            
            # Clicar no filtro "Easy Apply"
            easy_apply_filter = await self.page.wait_for_selector('text=Easy Apply', timeout=10000)
            if easy_apply_filter:
                await easy_apply_filter.click()
                await self.random_delay(2, 4)
                print("✅ Filtro Easy Apply aplicado!")
            else:
                print("⚠️ Filtro Easy Apply não encontrado")
                
        except Exception as e:
            print(f"❌ Erro ao filtrar Easy Apply: {e}")
    
    async def get_job_listings(self) -> List[Dict]:
        """Obtém lista de todas as vagas disponíveis na listagem, sem filtrar pelo botão Easy Apply"""
        try:
            print("📋 Obtendo lista de vagas...")
            job_selectors = [
                '.job-card-container',
                'li.jobs-search-results__list-item',
                'div.job-card-list__entity-lockup',
                'div.jobs-search-results__list-item',
                'li.job-card-container',
                'div[data-job-id]',
                'li[data-job-id]',
                'div.job-card-list__entity',
                'li.job-card-list__entity',
            ]
            job_cards = []
            for selector in job_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=8000)
                    job_cards = await self.page.query_selector_all(selector)
                    if job_cards:
                        print(f"✅ Encontradas {len(job_cards)} vagas usando seletor: {selector}")
                        break
                except Exception:
                    continue
            await self.page.screenshot(path='debug_linkedin.png')
            print("🖼️ Screenshot salvo como debug_linkedin.png para análise")
            if not job_cards:
                print("❌ Nenhuma vaga encontrada com os seletores conhecidos.")
                return []
            jobs = []
            for card in job_cards[:10]:  # Limitar a 10 vagas por vez
                try:
                    title_element = await card.query_selector('.job-card-list__title')
                    if not title_element:
                        title_element = await card.query_selector('a.job-card-list__title')
                    if not title_element:
                        title_element = await card.query_selector('h3.job-card-list__title')
                    if not title_element:
                        title_element = await card.query_selector('a[data-control-name="job_card_click"]')
                    company_element = await card.query_selector('.job-card-container__company-name')
                    if not company_element:
                        company_element = await card.query_selector('a.job-card-container__company-name')
                    if not company_element:
                        company_element = await card.query_selector('span.job-card-container__company-name')
                    if title_element and company_element:
                        title = await title_element.inner_text()
                        company = await company_element.inner_text()
                        jobs.append({
                            'title': title.strip(),
                            'company': company.strip(),
                            'element': card
                        })
                except Exception as e:
                    print(f"⚠️ Erro ao extrair vaga: {e}")
                    continue
            print(f"✅ {len(jobs)} vagas extraídas para candidatura.")
            return jobs
        except Exception as e:
            print(f"❌ Erro ao obter vagas: {e}")
            return []

    async def apply_to_job(self, job: Dict) -> bool:
        """Clica na vaga, procura o botão 'Candidatura simplificada' no painel lateral e segue o fluxo de candidatura"""
        try:
            await job['element'].click()
            await self.random_delay(2, 4)
            # Procurar o botão Easy Apply no painel lateral
            easy_apply_btn = None
            easy_apply_selectors = [
                'button[aria-label*="Candidatura simplificada"]',
                'button[aria-label*="Easy Apply"]',
                'button:has-text("Candidatura simplificada")',
                'button:has-text("Easy Apply")',
                'button.jobs-apply-button',
            ]
            for selector in easy_apply_selectors:
                easy_apply_btn = await self.page.query_selector(selector)
                if easy_apply_btn:
                    print(f"✅ Botão Easy Apply encontrado com seletor: {selector}")
                    break
            if not easy_apply_btn:
                print("⚠️ Botão Easy Apply não encontrado para esta vaga: {0} na {1}".format(job['title'], job['company']))
                return False
            await easy_apply_btn.click()
            await self.random_delay(2, 4)
            # Avançar por todas as etapas do formulário
            while True:
                avancar = await self.page.query_selector('button[aria-label*="Avançar"], button:has-text("Avançar"), button[aria-label*="Próxima"], button:has-text("Próxima")')
                if avancar:
                    await avancar.click()
                    await self.random_delay(1, 2)
                else:
                    break
            # Seleciona opções obrigatórias se existirem
            try:
                conhecimento = await self.page.query_selector('select[aria-label*="Possui conhecimento"]')
                if conhecimento:
                    await conhecimento.select_option("Yes")
                    await self.random_delay(1, 2)
            except Exception:
                pass
            # Clica em "Revisar" se existir
            try:
                revisar = await self.page.query_selector('button[aria-label*="Revisar"], button:has-text("Revisar")')
                if revisar:
                    await revisar.click()
                    await self.random_delay(1, 2)
            except Exception:
                pass
            # Clica em "Enviar candidatura"
            enviar = await self.page.query_selector('button[aria-label*="Enviar candidatura"], button:has-text("Enviar candidatura")')
            if enviar:
                await enviar.click()
                await self.random_delay(2, 3)
                print(f"✅ Candidatura enviada para: {job['title']} na {job['company']}")
                return True
            else:
                print("❌ Botão 'Enviar candidatura' não encontrado!")
                return False
        except Exception as e:
            print(f"❌ Erro ao aplicar para vaga: {e}")
            return False
    
    async def close_application_modal(self):
        """Fecha modal de candidatura se estiver aberto"""
        try:
            # Tentar fechar modal clicando fora ou no X
            close_button = await self.page.query_selector('button[aria-label="Dismiss"]')
            if close_button:
                await close_button.click()
                await self.random_delay()
        except:
            pass
    
    async def random_delay(self, min_seconds: float = 1, max_seconds: float = 3):
        """Adiciona delay aleatório para parecer mais humano"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    async def click_jobs_menu(self):
        """Clica no menu 'Vagas' na barra de navegação principal"""
        try:
            print("🔗 Procurando e clicando no menu 'Vagas'...")
            await self.page.wait_for_selector('a.global-nav__primary-link[href*="/jobs/"]', timeout=15000)
            await self.page.click('a.global-nav__primary-link[href*="/jobs/"]')
            await self.random_delay(2, 4)
            print("✅ Menu 'Vagas' acessado!")
            return True
        except Exception as e:
            print(f"❌ Não foi possível clicar no menu 'Vagas': {e}")
            return False

    async def run_automation(self):
        """Executa a automação completa"""
        try:
            print("🚀 Iniciando automação do LinkedIn...")
            # Verificar credenciais
            if not self.credentials.get('email') or not self.credentials.get('password'):
                print("❌ Configure suas credenciais no arquivo config.json")
                return
            # Iniciar navegador
            await self.start_browser()
            # Login
            if not await self.login_linkedin():
                return
            # Clicar no menu 'Vagas'
            if not await self.click_jobs_menu():
                return
            # Aplicar para vagas com diferentes keywords
            applications_count = 0
            max_applications = self.credentials.get('max_applications', 10)
            for keyword in self.credentials.get('keywords', []):
                if applications_count >= max_applications:
                    break
                for location in self.credentials.get('locations', [""]):
                    if applications_count >= max_applications:
                        break
                    print(f"\n🔍 Buscando: {keyword} em {location}")
                    await self.search_jobs(keyword, location)
                    jobs = await self.get_job_listings()
                    for job in jobs:
                        if applications_count >= max_applications:
                            break
                        print(f"📝 Aplicando para: {job['title']} na {job['company']}")
                        if await self.apply_to_job(job):
                            applications_count += 1
                            print(f"✅ Candidatura {applications_count}/{max_applications} enviada!")
                        await self.close_application_modal()
                        await self.random_delay(3, 6)
            print(f"\n🎉 Automação concluída! {applications_count} candidaturas enviadas.")
        except Exception as e:
            print(f"❌ Erro na automação: {e}")
        finally:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()

async def main():
    """Função principal"""
    automation = LinkedInAutomation(headless=False)  # False para ver o navegador
    await automation.run_automation()

if __name__ == "__main__":
    asyncio.run(main())
