---
title: Docker アプリケーションのトレース
kind: Documentation
aliases:
  - /ja/tracing/docker/
  - /ja/tracing/setup/docker/
  - /ja/agent/apm/docker
further_reading:
  - link: 'https://github.com/DataDog/datadog-agent/tree/master/pkg/trace'
    tag: Github
    text: ソースコード
  - link: '/integrations/amazon_ecs/#トレースの収集'
    tag: Documentation
    text: ECS アプリケーションをトレースする
  - link: /agent/docker/log/
    tag: Documentation
    text: アプリケーションログの収集
  - link: /agent/docker/integrations/
    tag: ドキュメント
    text: アプリケーションのメトリクスとログを自動で収集
  - link: /agent/guide/autodiscovery-management/
    tag: ドキュメント
    text: データ収集をコンテナのサブセットのみに制限
  - link: /agent/docker/tag/
    tag: ドキュメント
    text: コンテナから送信された全データにタグを割り当て
---
環境変数として `DD_APM_ENABLED=true` を渡すことで、`datadog/agent` コンテナで Trace Agent を有効にします。

## ホストからのトレース

`docker run` コマンドにオプション `-p 127.0.0.1:8126:8126/tcp` を追加すると、ポート `8126/tcp` で _自分のホストからのみ_ トレースを利用できます。

_任意のホスト_ からトレースを利用するには、`-p 8126:8126/tcp` を使用します。

たとえば、次のコマンドを使用すると、Agent はユーザーのホストからのみトレースを受信します。

{{< tabs >}}
{{% tab "標準" %}}

```shell
docker run -d -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -p 127.0.0.1:8126:8126/tcp \
              -e DD_API_KEY="<DATADOG_API_キー>" \
              -e DD_APM_ENABLED=true \
              datadog/agent:latest
```

{{% /tab %}}
{{% tab "Windows" %}}

```shell
docker run -d -p 127.0.0.1:8126:8126/tcp \
              -e DD_API_KEY="<API_キー>" \
              -e DD_APM_ENABLED=true \
              datadog/agent:latest
```

{{% /tab %}}
{{< /tabs >}}

## Docker APM Agent の環境変数

Docker Agent 内のトレースに利用可能なすべての環境変数をリストします。

| 環境変数       | 説明                                                                                                                                                                                                                                                                                                                                          |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DD_API_KEY`               | [Datadog API キー][1]                                                                                                                                                                                                                                                                                                                                 |
| `DD_PROXY_HTTPS`           | 使用するプロキシの URL をセットアップします。                                                                                                                                                                                                                                                                                                                 |
| `DD_APM_REPLACE_TAGS`      | [スパンのタグから機密データをスクラブします][2]。                                                                                                                                                                                                                                                                                                     |
| `DD_HOSTNAME`              | 自動検出が失敗した場合、または Datadog Cluster Agent を実行する場合に、メトリクスに使用するホスト名を手動で設定します。                                                                                                                                                                                                                                        |
| `DD_DOGSTATSD_PORT`        | DogStatsD ポートを設定します。                                                                                                                                                                                                                                                                                                                              |
| `DD_APM_RECEIVER_SOCKET`   | 設定した場合、Unix Domain Sockets からトレースを収集し、ホスト名とポートコンフィギュレーションよりも優先します。デフォルトでは設定されていません。設定する場合は、有効な sock ファイルを指定する必要があります。                                                                                                                                                                       |
| `DD_BIND_HOST`             | StatsD とレシーバーのホスト名を設定します。                                                                                                                                                                                                                                                                                                                  |
| `DD_LOG_LEVEL`             | ログレベルを設定します。(`trace`/`debug`/`info`/`warn`/`error`/`critical`/`off`)                                                                                                                                                                                                                                                                      |
| `DD_APM_ENABLED`           | `true` に設定すると、Datadog Agent はトレースメトリクスを受け付けます。                                                                                                                                                                                                                                                                                         |
| `DD_APM_CONNECTION_LIMIT`  | 30 秒のタイムウィンドウに対する最大接続数の上限を設定します。デフォルトの上限は 2000 です。                                                                                                                                                                                                                                                    |
| `DD_APM_DD_URL`            | トレースが送信される Datadog API エンドポイント。Datadog EU サイトの場合は、`DD_APM_DD_URL` を `https://trace.agent.datadoghq.eu` に設定します                                                                                                                                                                                                                            |
| `DD_APM_RECEIVER_PORT`     | Datadog Agent のトレースレシーバーがリスニングするポート。デフォルト値は `8126` です。                                                                                                                                                                                                                                                                    |
| `DD_APM_NON_LOCAL_TRAFFIC` | [他のコンテナからのトレース](#tracing-from-other-containers)時に、非ローカルトラフィックを許可します。                                                                                                                                                                                                                                                        |
| `DD_APM_IGNORE_RESOURCES`  | Agent が無視するリソースを構成します。書式はカンマ区切りの正規表現です。例: <code>GET /ignore-me,(GET\|POST) /and-also-me</code> となります。                                                                                                                                                                                       |
| `DD_APM_ANALYZED_SPANS`    | トランザクションを分析するスパンを構成します。書式はカンマ区切りのインスタンス <code>\<サービス名>\|;\<オペレーション名>=1</code>、たとえば、<code>my-express-app\|;express.request=1,my-dotnet-app\|;aspnet_core_mvc.request=1</code> となります。トレーシングクライアントでコンフィギュレーションパラメーターを使用して[自動的に有効化][3]することもできます。 |
| `DD_APM_MAX_EPS`           | 1 秒あたりの最大 Analyzed Span 数を設定します。デフォルトは 1 秒あたり 200 イベントです。                                                                                                                                                                                                                                                                        |
| `DD_APM_MAX_TPS`           | 1 秒あたりの最大トレース数を設定します。デフォルトは 1 秒あたり 10 トレースです。                                                                                                                                                                                                                                                                                 |

## 他のコンテナからのトレース

DogStatsD と同様に、[Docker ネットワーク](#docker-network)または [Docker ホスト IP](#docker-host-ip) を使用して、他のコンテナから Agent にトレースを送信できます。

### Docker ネットワーク

最初に、ユーザー定義のブリッジネットワークを作成します。

```bash
docker network create <NETWORK_NAME>
```

次に、先ほど作成したネットワークに接続されている Agent とアプリケーションコンテナを起動します。

{{< tabs >}}
{{% tab "標準" %}}

```bash
# Datadog Agent
docker run -d --name datadog-agent \
              --network <ネットワーク名> \
              -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -e DD_API_KEY="<DATADOG_API_キー>" \
              -e DD_APM_ENABLED=true \
              -e DD_APM_NON_LOCAL_TRAFFIC=true \
              datadog/agent:latest

# アプリケーション
docker run -d --name app \
              --network <ネットワーク名> \
              company/app:latest
```

{{% /tab %}}
{{% tab "Windows" %}}

```bash
# Datadog Agent
docker run -d --name datadog-agent \
              --network "<ネットワーク名>" \
              -e DD_API_KEY="<API_キー>" \
              -e DD_APM_ENABLED=true \
              -e DD_APM_NON_LOCAL_TRAFFIC=true \
              datadog/agent:latest

# Application
docker run -d --name app \
              --network "<ネットワーク名>" \
              company/app:latest
```

{{% /tab %}}
{{< /tabs >}}

これで `app` コンテナ内のホスト名 `datadog-agent` が公開されます。
`docker-compose` を使用している場合、`<NETWORK_NAME>` パラメーターは、`docker-compose.yml` の `networks` セクションに定義されている名前になります。

このアドレスにトレースを送信するには、アプリケーショントレーサーを構成する必要があります。アプリケーションコンテナで、Agent コンテナ名として `DD_AGENT_HOST`、Agent Trace ポートとして `DD_TRACE_AGENT_PORT` を使用して、環境変数を設定します。(この例では、それぞれ `datadog-agent` と `8126` です。)

または、サポートされている言語ごとに、以下の例を参照して Agent ホストを手動で設定します。

{{< tabs >}}
{{% tab "Java" %}}
環境変数を使用して Java Agent 構成を更新します。

```bash
DD_AGENT_HOST=datadog-agent \
DD_TRACE_AGENT_PORT=8126 \
java -javaagent:/path/to/the/dd-java-agent.jar -jar /your/app.jar
```

または、システムプロパティを使用して更新します。

```bash
java -javaagent:/path/to/the/dd-java-agent.jar \
     -Ddd.agent.host=datadog-agent \
     -Ddd.agent.port=8126 \
     -jar /your/app.jar
```

{{% /tab %}}
{{% tab "Python" %}}

```python
from ddtrace import tracer

tracer.configure(
    hostname='datadog-agent',
    port=8126,
)
```

{{% /tab %}}
{{% tab "Ruby" %}}

```ruby
Datadog.configure do |c|
  c.tracer hostname: 'datadog-agent',
           port: 8126
end
```

{{% /tab %}}
{{% tab "Go" %}}

```go
package main

import "gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"

func main() {
    tracer.Start(tracer.WithAgentAddr("datadog-agent:8126"))
    defer tracer.Stop()
}
```

{{% /tab %}}
{{% tab "Node.js" %}}

```javascript
const tracer = require('dd-trace').init({
    hostname: 'datadog-agent',
    port: 8126
});
```

{{% /tab %}}

{{% tab ".NET" %}}

インスツルメンテーションされたアプリを起動する前に変数を設定します。

```bash
# 環境変数
export CORECLR_ENABLE_PROFILING=1
export CORECLR_PROFILER={846F5F1C-F9AE-4B07-969E-05C26BC060D8}
export CORECLR_PROFILER_PATH=/opt/datadog/Datadog.Trace.ClrProfiler.Native.so
export DD_INTEGRATIONS=/opt/datadog/integrations.json
export DD_DOTNET_TRACER_HOME=/opt/datadog

# コンテナ
export DD_AGENT_HOST=datadog-agent
export DD_TRACE_AGENT_PORT=8126

# アプリケーションの開始
dotnet example.dll
```

{{% /tab %}}
{{< /tabs >}}

### Docker ホスト IP

Agent コンテナポート `8126` は、直接ホストにリンクしている必要があります。
このコンテナのデフォルトのルートにレポートを送信するようにアプリケーショントレーサーを構成します (デフォルトのルートは `ip route` コマンドを使用して決定)。

次の Python Tracer の例では、デフォルトのルートを `172.17.0.1` と仮定しています。

```python
from ddtrace import tracer

tracer.configure(hostname='172.17.0.1', port=8126)
```

## その他の参考資料

{{< partial name="whats-next/whats-next.html" >}}

[1]: https://app.datadoghq.com/account/settings#api
[2]: /ja/tracing/guide/security/#replace-rules
[3]: /ja/tracing/app_analytics/#automatic-configuration