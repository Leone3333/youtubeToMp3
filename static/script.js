let lim = 5
    div_input_url = document.getElementById("div-input-url-id")
    new_url_input = document.getElementById("input-url-id")
    btn_inserir_url = document.getElementById("btn-inserir-url-id")
    btn_converter = document.getElementById("btn-converter-id")
    div_loading = document.getElementById("loading-id")
    
    btn_inserir_url.addEventListener('click', () => {
        if (lim == 0) {
            alert("Limite de 5 urls atingido!")
        }else{
            if(new_url_input.type == "text"){
                let copia_input = new_url_input.cloneNode(true)
                copia_input.value = ""
                div_input_url.appendChild(copia_input)
            }else{
                new_url_input.type = "text"
            }
            lim-=1
        }
    })
    
    // ao clicar o botão ativa o evento de converter
    btn_converter.addEventListener("click", () => {
        // reseta o limitador
        lim = 5
        // todos os inputs para url criados 
        urls = document.querySelectorAll('.input-url-class')
        
        // todos o conteudos dentro dos inputs em forma de array
        urls_data = get_urls(urls)
        
        // torna tela de carregamento visivel
        div_loading.style.display = 'block'
        
        // lida com requisições http
        fetch('/converter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({dados: urls_data})
        })
        // lida com as repostas da requisição http
        .then(response => response.json())
        .then(data => {
            
            // tira a tela de carregamento 
            div_loading.style.display = 'none'
            
            // limpar inputs de urls
            clean_urls(urls)

            // feedback do backend python 
            if (data.message) {
                alert(data.message)
            }
            if (data.error) {
                alert(data.error)
            }

        })
        .catch(error => {
            alert("Erro: " + error)
        })
    })

    // captura todas as urls dos campos criados
    const get_urls = (urls) => {
        data = []
        urls.forEach(url => {
            if (url.value != "") {
                data.push(url.value)
            } else {
                alert("Insira urls validas")
            }
        });
        console.log("Função ativada, dados coletados: " + data)
        return data
    }

    // limpa os campos de url e remove eles do front
    const clean_urls = (urls) => {
        urls.forEach(url => {
            console.log("Limpar " + url)
            url.value = ''
        })
        div_input_url.innerHTML = "";
    }
