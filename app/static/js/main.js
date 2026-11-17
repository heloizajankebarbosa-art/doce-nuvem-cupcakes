// Doce Nuvem Cupcakes - interações do front-end
(function () {
  "use strict";

  // Menu no celular
  const botaoMenu = document.querySelector("[data-menu]");
  const menu = document.querySelector(".menu");
  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", () => {
      const aberto = menu.classList.toggle("aberto");
      botaoMenu.setAttribute("aria-expanded", aberto);
    });
  }

  // Fechar mensagens
  document.querySelectorAll("[data-fechar]").forEach((b) =>
    b.addEventListener("click", () => b.closest(".alerta").remove())
  );

  // FB-03: ao voltar para um cupcake da vitrine (#produto-N), a mensagem aparece flutuando
  // na tela, para a pessoa ver o aviso sem precisar subir a página
  const avisos = document.querySelector(".mensagens");
  if (avisos && /^#produto-\d+$/.test(window.location.hash)) {
    avisos.classList.add("flutuante");
    setTimeout(() => avisos.classList.add("sumindo"), 3500);
    setTimeout(() => avisos.remove(), 4000);
  }

  // FB-04: botões − e + para escolher a quantidade antes de adicionar ao carrinho
  document.querySelectorAll("[data-seletor]").forEach((seletor) => {
    const campo = seletor.querySelector("input");
    const menos = seletor.querySelector("[data-menos]");
    const mais = seletor.querySelector("[data-mais]");
    const min = parseInt(campo.min || "1", 10);
    const max = parseInt(campo.max || "99", 10);
    function ajustar(valor) {
      const n = Math.min(max, Math.max(min, parseInt(valor, 10) || min));
      campo.value = n;
      menos.disabled = n <= min;
      mais.disabled = n >= max;
    }
    menos.addEventListener("click", () => ajustar(parseInt(campo.value, 10) - 1));
    mais.addEventListener("click", () => ajustar(parseInt(campo.value, 10) + 1));
    campo.addEventListener("change", () => ajustar(campo.value));
    ajustar(campo.value);
  });

  // Confirmação antes de ações que não têm volta (ex.: cancelar pedido)
  document.querySelectorAll("form[data-confirmar]").forEach((form) =>
    form.addEventListener("submit", (e) => {
      if (!window.confirm(form.dataset.confirmar)) e.preventDefault();
    })
  );

  // Validação no navegador: mostra o erro embaixo do campo, antes de enviar
  function mensagemDoCampo(campo) {
    if (campo.validity.valueMissing) return "Preencha este campo.";
    if (campo.validity.typeMismatch && campo.type === "email") return "Digite um e-mail válido.";
    if (campo.validity.tooShort) return `Use pelo menos ${campo.minLength} caracteres.`;
    if (campo.validity.rangeUnderflow) return `O valor mínimo é ${campo.min}.`;
    return "";
  }
  function marcar(campo) {
    let aviso = campo.parentElement.querySelector(".erro-campo[data-para='" + campo.id + "']");
    const msg = campo.offsetParent === null ? "" : mensagemDoCampo(campo); // ignora campos escondidos
    campo.classList.toggle("invalido", !!msg);
    campo.setAttribute("aria-invalid", !!msg);
    if (msg && !aviso) {
      aviso = document.createElement("span");
      aviso.className = "erro-campo";
      aviso.dataset.para = campo.id;
      aviso.id = "erro-" + campo.id;
      campo.setAttribute("aria-describedby", aviso.id);
      campo.insertAdjacentElement("afterend", aviso);
    }
    if (aviso) aviso.textContent = msg;
    return !msg;
  }
  document.querySelectorAll("form[data-validar]").forEach((form) => {
    form.querySelectorAll("input[required], select[required]").forEach((c) => {
      c.addEventListener("blur", () => marcar(c));
      // enquanto digita, some com o erro assim que o campo fica certo
      c.addEventListener("input", () => { if (c.classList.contains("invalido")) marcar(c); });
    });
    form.addEventListener("submit", (e) => {
      const campos = [...form.querySelectorAll("input[required], select[required]")];
      const invalidos = campos.filter((c) => !marcar(c));
      const senha = form.querySelector("#senha"), conf = form.querySelector("#confirmacao");
      if (senha && conf && senha.value !== conf.value) {
        conf.setCustomValidity("x");
        invalidos.push(conf);
        conf.classList.add("invalido");
        alertaCampo(conf, "As senhas não são iguais.");
      } else if (conf) conf.setCustomValidity("");
      if (invalidos.length) { e.preventDefault(); invalidos[0].focus(); }
    });
  });
  function alertaCampo(campo, texto) {
    let aviso = campo.parentElement.querySelector(".erro-campo[data-para='" + campo.id + "']");
    if (!aviso) {
      aviso = document.createElement("span");
      aviso.className = "erro-campo"; aviso.dataset.para = campo.id;
      campo.insertAdjacentElement("afterend", aviso);
    }
    aviso.textContent = texto;
  }

  // Checkout: mostra/esconde endereço e cartão e recalcula o total
  const checkout = document.getElementById("form-checkout");
  if (checkout) {
    const blocoEndereco = document.getElementById("bloco-endereco");
    const blocoCartao = document.getElementById("bloco-cartao");
    const infoPix = document.getElementById("info-pix");
    const taxaEl = document.getElementById("valor-taxa");
    const totalEl = document.getElementById("valor-total");
    const moeda = (v) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

    function atualizar() {
      const tipo = checkout.querySelector("[name=tipo_entrega]:checked").value;
      const forma = checkout.querySelector("[name=forma_pagamento]:checked").value;
      const taxa = tipo === "entrega" ? parseFloat(taxaEl.dataset.taxa) : 0;
      blocoEndereco.hidden = tipo !== "entrega";
      blocoCartao.hidden = forma !== "cartao";
      infoPix.hidden = forma !== "pix";
      document.getElementById("endereco").required = tipo === "entrega";
      ["numero_cartao", "validade", "cvv"].forEach((id) =>
        (document.getElementById(id).required = forma === "cartao")
      );
      taxaEl.textContent = moeda(taxa);
      totalEl.textContent = moeda(parseFloat(totalEl.dataset.subtotal) + taxa);
    }
    checkout.addEventListener("change", atualizar);
    atualizar();

    // Máscaras simples
    const num = document.getElementById("numero_cartao");
    num.addEventListener("input", () => {
      num.value = num.value.replace(/\D/g, "").slice(0, 16).replace(/(\d{4})(?=\d)/g, "$1 ");
    });
    const val = document.getElementById("validade");
    val.addEventListener("input", () => {
      val.value = val.value.replace(/\D/g, "").slice(0, 4).replace(/(\d{2})(\d)/, "$1/$2");
    });
  }
})();
