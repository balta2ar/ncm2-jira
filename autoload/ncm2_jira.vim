if get(s:, 'loaded', 0)
    finish
endif
let s:loaded = 1

let g:ncm2_jira_enabled = get(g:, 'ncm2_jira_enabled',  1)

let g:ncm2_jira#proc = yarp#py3('ncm2_jira')

let g:ncm2_jira#source = get(g:, 'ncm2_jira#jira_source', {
            \ 'name': 'jira',
            \ 'priority': 9,
            \ 'mark': 'jira',
            \ 'sorter': 'custom',
            \ 'filter': 'fuzzybydate',
            \ 'word_pattern': 'JI\w*',
            \ 'complete_pattern': 'JI\w*',
            \ 'matcher': {'key': 'custom'},
            \ 'on_complete': 'ncm2_jira#on_complete',
            \ 'on_warmup': 'ncm2_jira#on_warmup'
            \ })

let g:ncm2_jira#source = extend(g:ncm2_jira#source,
            \ get(g:, 'ncm2_jira#source_override', {}),
            \ 'force')

function! ncm2_jira#init()
    call ncm2#register_source(g:ncm2_jira#source)
endfunction

function! ncm2_jira#on_warmup(ctx)
    call g:ncm2_jira#proc.jobstart()
endfunction

function! ncm2_jira#on_complete(ctx)
    let s:is_enabled = get(b:, 'ncm2_jira_enabled',
                \ get(g:, 'ncm2_jira_enabled', 1))
    if ! s:is_enabled
        return
    endif
    call g:ncm2_jira#proc.try_notify('on_complete', a:ctx)
endfunction
