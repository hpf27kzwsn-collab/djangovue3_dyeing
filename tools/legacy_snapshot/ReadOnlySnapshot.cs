using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Globalization;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Data.SqlTypes;

public static class ErpReadOnlySnapshot {
    static void Text(TextWriter writer,string text) {
        writer.Write('"');
        foreach(char c in text) {
            if(c=='"'||c=='\\') {writer.Write('\\');writer.Write(c);}
            else if(c<32||c>126) {writer.Write("\\u");writer.Write(((int)c).ToString("x4",CultureInfo.InvariantCulture));}
            else writer.Write(c);
        }
        writer.Write('"');
    }
    static void Value(TextWriter writer,object value) {
        if(value==DBNull.Value) {writer.Write("null");return;}
        if(value is SqlDecimal) {
            var number=(SqlDecimal)value;
            if(number.IsNull) writer.Write("null");else Text(writer,number.ToString());
            return;
        }
        if(value is bool) {writer.Write((bool)value?"true":"false");return;}
        if(value is byte[]) {Text(writer,Convert.ToBase64String((byte[])value));return;}
        if(value is DateTime) {Text(writer,((DateTime)value).ToString("O",CultureInfo.InvariantCulture));return;}
        if(value is DateTimeOffset) {Text(writer,((DateTimeOffset)value).ToString("O",CultureInfo.InvariantCulture));return;}
        if(value is double) {Text(writer,((double)value).ToString("R",CultureInfo.InvariantCulture));return;}
        if(value is float) {Text(writer,((float)value).ToString("R",CultureInfo.InvariantCulture));return;}
        if(value is IFormattable) {Text(writer,((IFormattable)value).ToString(null,CultureInfo.InvariantCulture));return;}
        Text(writer,(string)value);
    }
    static string Identifier(string name) {return "["+name.Replace("]","]]")+"]";}
    public static long Export(DbConnection connection,string schema,string table,string[] columns,string[] keys,string path) {
        using(var command=connection.CreateCommand()) {
            var selected=new List<string>();foreach(var column in columns) selected.Add(Identifier(column));
            command.CommandText="SELECT "+string.Join(",",selected)+" FROM "+Identifier(schema)+"."+Identifier(table);
            if(keys.Length>0) {var ordered=new List<string>();foreach(var key in keys) ordered.Add(Identifier(key));command.CommandText+=" ORDER BY "+string.Join(",",ordered);}
            command.CommandTimeout=0;
            using(var reader=command.ExecuteReader())
            using(var stream=new FileStream(path,FileMode.CreateNew,FileAccess.Write,FileShare.Read,1024*1024))
            using(var writer=new StreamWriter(stream,new UTF8Encoding(false),1024*1024))
            using(var index=new StreamWriter(path+".index",false,new UTF8Encoding(false))) {
                writer.NewLine="\n";index.NewLine="\n";
                long row=0;index.WriteLine("0,0");
                var values=new object[reader.FieldCount];
                while(reader.Read()) {
                    for(int c=0;c<reader.FieldCount;c++) {
                        string type=reader.GetDataTypeName(c);
                        values[c]=(type=="decimal"||type=="numeric")?reader.GetProviderSpecificValue(c):reader.GetValue(c);
                    }
                    row++;
                    writer.Write("{\"row\":");writer.Write(row.ToString(CultureInfo.InvariantCulture));writer.Write(",\"key\":");
                    if(keys.Length==0) writer.Write("null");
                    else {writer.Write('{');for(int k=0;k<keys.Length;k++) {if(k>0)writer.Write(',');Text(writer,keys[k]);writer.Write(':');Value(writer,values[reader.GetOrdinal(keys[k])]);}writer.Write('}');}
                    writer.Write(",\"values\":{");
                    for(int c=0;c<columns.Length;c++) {if(c>0)writer.Write(',');Text(writer,columns[c]);writer.Write(':');Value(writer,values[c]);}
                    writer.WriteLine("}}");
                    if(row%1000==0) {writer.Flush();index.WriteLine(row.ToString(CultureInfo.InvariantCulture)+","+stream.Position.ToString(CultureInfo.InvariantCulture));}
                }
                return row;
            }
        }
    }
}
