
    /* Botão de esconder/mostrar sidebar inteira */
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

    /* Animação cascata de todas as abas de categoria (genérica) */
    const titulos = document.querySelectorAll('.categoria-titulo');
    titulos.forEach((titulo) => {
      const lista = titulo.nextElementSibling;
      if (!lista || !lista.classList.contains('lista-topicos')) return;
      if (titulo.id.startsWith('serie-')) return;

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

  /* Animação cascata da série Operação Prato */
  const serieBtnOperacaoPrato = document.getElementById('serie-operacao-prato');
  const serieListaOperacaoPrato = document.getElementById('capitulos-operacao-prato');
  if (serieBtnOperacaoPrato && serieListaOperacaoPrato) {
    const serieItensOperacaoPrato = Array.from(serieListaOperacaoPrato.querySelectorAll('li'));

    function abrirSerieOperacaoPrato() {
      serieListaOperacaoPrato.style.display = 'block';
      serieListaOperacaoPrato.style.visibility = 'visible';
      void serieListaOperacaoPrato.offsetHeight;
      serieItensOperacaoPrato.forEach((li, idx) => {
        li.style.animation = 'none';
        li.offsetHeight;
        li.style.animation = 'slideFadeIn 0.3s ease forwards';
        li.style.animationDelay = `${idx * 60}ms`;
      });
      serieBtnOperacaoPrato.setAttribute('aria-expanded', 'true');
    }

    function fecharSerieOperacaoPrato() {
      const ultimo = serieItensOperacaoPrato.length - 1;
      serieItensOperacaoPrato.forEach((li, idx) => {
        li.style.animation = 'none';
        li.offsetHeight;
        li.style.animation = 'slideFadeOut 0.2s ease forwards';
        li.style.animationDelay = `${idx * 50}ms`;
      });
      setTimeout(() => {
        serieListaOperacaoPrato.style.display = 'none';
        serieListaOperacaoPrato.style.visibility = 'hidden';
        serieItensOperacaoPrato.forEach(li => { li.style.animation = 'none'; });
      }, ultimo * 50 + 200);
      serieBtnOperacaoPrato.setAttribute('aria-expanded', 'false');
    }

    serieBtnOperacaoPrato.addEventListener('click', () => {
      const aberto = serieListaOperacaoPrato.style.display === 'block';
      if (aberto) { fecharSerieOperacaoPrato(); } else { abrirSerieOperacaoPrato(); }
    });

    serieBtnOperacaoPrato.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        serieBtnOperacaoPrato.click();
      }
    });
  };

  /* Animação cascata da série Continentes Perdidos */
  const serieBtnContinentesPerdidos = document.getElementById('serie-continentes-perdidos');
  const serieListaContinentesPerdidos = document.getElementById('capitulos-continentes-perdidos');
  if (serieBtnContinentesPerdidos && serieListaContinentesPerdidos) {
    const serieItensContinentesPerdidos = Array.from(serieListaContinentesPerdidos.querySelectorAll('li'));

    function abrirSerieContinentesPerdidos() {
      serieListaContinentesPerdidos.style.display = 'block';
      serieListaContinentesPerdidos.style.visibility = 'visible';
      void serieListaContinentesPerdidos.offsetHeight;
      serieItensContinentesPerdidos.forEach((li, idx) => {
        li.style.animation = 'none';
        li.offsetHeight;
        li.style.animation = 'slideFadeIn 0.3s ease forwards';
        li.style.animationDelay = `${idx * 60}ms`;
      });
      serieBtnContinentesPerdidos.setAttribute('aria-expanded', 'true');
    }

    function fecharSerieContinentesPerdidos() {
      const ultimo = serieItensContinentesPerdidos.length - 1;
      serieItensContinentesPerdidos.forEach((li, idx) => {
        li.style.animation = 'none';
        li.offsetHeight;
        li.style.animation = 'slideFadeOut 0.2s ease forwards';
        li.style.animationDelay = `${idx * 50}ms`;
      });
      setTimeout(() => {
        serieListaContinentesPerdidos.style.display = 'none';
        serieListaContinentesPerdidos.style.visibility = 'hidden';
        serieItensContinentesPerdidos.forEach(li => { li.style.animation = 'none'; });
      }, ultimo * 50 + 200);
      serieBtnContinentesPerdidos.setAttribute('aria-expanded', 'false');
    }

    serieBtnContinentesPerdidos.addEventListener('click', () => {
      const aberto = serieListaContinentesPerdidos.style.display === 'block';
      if (aberto) { fecharSerieContinentesPerdidos(); } else { abrirSerieContinentesPerdidos(); }
    });

    serieBtnContinentesPerdidos.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        serieBtnContinentesPerdidos.click();
      }
    });
  };
