
        const btn = document.getElementById('btnToggleSidebar');
        const shell = document.querySelector('.site-shell');
        btn.addEventListener('click', () => {
          shell.classList.toggle('sidebar-hidden');
          if (shell.classList.contains('sidebar-hidden')) {
            btn.textContent = '≡';
            btn.setAttribute('aria-label', 'Mostrar barra lateral');
          } else {
            btn.textContent = '☰';
            btn.setAttribute('aria-label', 'Esconder barra lateral');
          }
        });
        const titulos = document.querySelectorAll('.categoria-titulo');
        titulos.forEach((titulo) => {
          const lista = titulo.nextElementSibling;
          if (!lista || !lista.classList.contains('lista-topicos')) return;
          if (titulo.id === 'serie-continentes-perdidos') return;
          const itens = Array.from(lista.querySelectorAll('li'));
          function abrir() {
            lista.style.display = 'block';
            lista.style.visibility = 'visible';
            void lista.offsetHeight;
            itens.forEach((li, i) => {
              li.style.animation = 'none';
              li.offsetHeight;
              li.style.animation = 'slideFadeIn 0.3s ease forwards';
              li.style.animationDelay = `${i * 70}ms`;
            });
            titulo.setAttribute('aria-expanded', 'true');
          }
          function fechar() {
            const ultimo = itens.length - 1;
            itens.forEach((li, i) => {
              li.style.animation = 'none';
              li.offsetHeight;
              li.style.animation = 'slideFadeOut 0.2s ease forwards';
              li.style.animationDelay = `${i * 60}ms`;
            });
            setTimeout(() => {
              lista.style.display = 'none';
              lista.style.visibility = 'hidden';
              itens.forEach(li => { li.style.animation = 'none'; });
            }, ultimo * 60 + 250);
            titulo.setAttribute('aria-expanded', 'false');
          }
          titulo.addEventListener('click', () => {
            const aberto = lista.style.display === 'block';
            if (aberto) { fechar(); } else { abrir(); }
          });
          titulo.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              titulo.click();
            }
          });
        });
        const serieBtn = document.getElementById('serie-continentes-perdidos');
        const serieLista = document.getElementById('capitulos-continentes-perdidos');
        if (serieBtn && serieLista) {
          const serieItens = Array.from(serieLista.querySelectorAll('li'));
          function abrirSerie() {
            serieLista.style.display = 'block';
            serieLista.style.visibility = 'visible';
            void serieLista.offsetHeight;
            serieItens.forEach((li, i) => {
              li.style.animation = 'none';
              li.offsetHeight;
              li.style.animation = 'slideFadeIn 0.3s ease forwards';
              li.style.animationDelay = `${i * 60}ms`;
            });
            serieBtn.setAttribute('aria-expanded', 'true');
          }
          function fecharSerie() {
            const ultimo = serieItens.length - 1;
            serieItens.forEach((li, i) => {
              li.style.animation = 'none';
              li.offsetHeight;
              li.style.animation = 'slideFadeOut 0.2s ease forwards';
              li.style.animationDelay = `${i * 50}ms`;
            });
            setTimeout(() => {
              serieLista.style.display = 'none';
              serieLista.style.visibility = 'hidden';
              serieItens.forEach(li => { li.style.animation = 'none'; });
            }, ultimo * 50 + 200);
            serieBtn.setAttribute('aria-expanded', 'false');
          }
          serieBtn.addEventListener('click', () => {
            const aberto = serieLista.style.display === 'block';
            if (aberto) { fecharSerie(); } else { abrirSerie(); }
          });
          serieBtn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              serieBtn.click();
            }
          });
        }
        const btnVoltar = document.getElementById('btnVoltar');
        if (btnVoltar) {
          btnVoltar.addEventListener('click', () => {
            window.location.href = '../index.html';
          });
        }
      