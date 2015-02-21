_file-server_completion() {
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _FILE_SERVER_COMPLETE=complete $1 ) )
    return 0
}

complete -F _file-server_completion -o default file-server;
