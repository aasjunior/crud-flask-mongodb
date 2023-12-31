$(document).ready(function() {
    $('#adicionar').click(function() {
        var medicamento = $('#medicamento').val()
        var quantidade = $('#quantidade').val()
        if (medicamento && quantidade) {
            var medicamentoItem = '<div class="medicamento-item">' +
                '<label for="medicamento">Medicamento</label>' +
                '<input type="text" name="medicamentos[][nome]" value="' + medicamento + '">' +
                '<label for="quantidade">Quantidade</label>' +
                '<input type="number" name="medicamentos[][quantidade]" value="' + quantidade + '">' +
                '<button type="button" class="remover">Remover</button>' +
                '</div>'
            $('#lista-medicamentos').append(medicamentoItem)
            $('#medicamento').val('')
            $('#quantidade').val('')

            // Atualize os dados da sessão ao adicionar um novo campo
            updateSessionData()
        }
    });

    // Adicione um evento de clique delegado para o elemento #lista-medicamentos
    $('#lista-medicamentos').on('click', '.remover', function() {
        $(this).closest('.medicamento-item').remove()

        // Atualize os dados da sessão ao remover um campo
        updateSessionData()
    });

    // Função para atualizar os dados na sessão
    function updateSessionData() {
        var medicamentos = []
        $('.medicamento-item').each(function() {
            medicamentos.push({
                'nome': $(this).find('input[name="medicamentos[][nome]"]').val(),
                'quantidade': $(this).find('input[name="medicamentos[][quantidade]"]').val()
            })
        })
        sessionData = { 'medicamentos': medicamentos }
        // Atualize os dados na sessão
        $.ajax({
            url: '/save-patient-diagnosis',
            type: 'post',
            data: JSON.stringify(sessionData),
            contentType: 'application/json',
            success: function() {
                // Dados atualizados na sessão
            }
        })
    }

    // Atualize os dados da sessão ao clicar em "Voltar"
    $('#voltar').click(function(e) {
        e.preventDefault()
        updateSessionData()
        window.location.href = '/patient'
    })
})
