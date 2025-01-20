DefineExpression -> Identifier<def> Identifier<hello> Round<FlatExpression -> Identifier<name> Operator<:> Identifier<str> |> Operator<:> Curly<> |
DefineExpression -> Identifier<def> Identifier<hello> Round<FlatExpression -> Identifier<name> Operator<:> Identifier<str> |> Operator<->> Identifier<None> Operator<:> Curly<> |
DefineExpression -> Identifier<class> Identifier<Name> Operator<:> Curly<> |
DefineExpression -> Identifier<class> Identifier<Name> Round<ElementExpression -> Identifier<Hello>> Operator<:> Curly<> |
DefineExpression -> Identifier<class> Identifier<Name> Square<ElementExpression -> Identifier<T>> Operator<:> Curly<> |
DefineExpression -> Identifier<class> Identifier<Name> Square<ElementExpression -> Identifier<T>> Round<ElementExpression -> Identifier<Hello>> Operator<:> Curly<> |
CallExpression -> Identifier<hello> Round<ElementExpression -> String<"John">> |
CallExpression -> Identifier<Name> Round<ElementExpression -> String<"John">> |
CallExpression -> Identifier<Name> Square<ElementExpression -> Identifier<str>> Round<ElementExpression -> String<"John">> |
FlatExpression -> Identifier<boolean> Operator<=> Identifier<true> |
FlatExpression -> Identifier<null> Operator<=> Identifier<none> |
FlatExpression -> Identifier<sum> Operator<=> IntegerDecimal<1> Operator<+> IntegerDecimal<2> |
FlatExpression -> Identifier<name> Operator<=> CallExpression -> Identifier<John> Round<ElementExpression -> String<"Wow">> | Operator<+> String<"Hello"> |
FlatExpression -> Identifier<name> Operator<=> CallExpression -> Identifier<John> Square<ElementExpression -> Identifier<int>> Round<ElementExpression -> String<"Wow">> | Operator<+> String<"Hello"> |
FlatExpression -> Identifier<name> Operator<.> CallExpression -> Identifier<print> Round<ElementExpression -> String<"Hello">> | |