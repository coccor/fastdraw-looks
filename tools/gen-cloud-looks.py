# Writes azure.look, aws.look and gcp.look: FastDraw's built-in look (tools/base-styles.txt) in each cloud's colours and type,
# with group styles for the cloud's boundaries and the cloud's own icons in place of the built-in ones.
# The style names, box sizes and type sizes stay the built-in look's, so a diagram drawn for it switches with one line.
#   python3 tools/gen-cloud-looks.py
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')

# Fonts from Fontsource, served by jsDelivr at a fixed version (the addresses FastDraw's look guide lists as checked).
FONTS = {
    'Open Sans': 'https://cdn.jsdelivr.net/fontsource/fonts/open-sans@5.3.0/latin-{weight}-{style}.ttf',
    'Inter': 'https://cdn.jsdelivr.net/fontsource/fonts/inter@5.3.0/latin-{weight}-{style}.ttf',
    'Roboto': 'https://cdn.jsdelivr.net/fontsource/fonts/roboto@5.3.0/latin-{weight}-{style}.ttf',
}

# ---- statements -------------------------------------------------------------------------------------------
# The base is a list of statements: a line and the indented lines that continue it, with the comments between.

def statements(text):
    out = []
    for line in text.split('\n'):
        if line.startswith((' ', '\t')) and out and out[-1][0] == 'style':
            out[-1][1].append(line)
        elif line.startswith('style '):
            out.append(('style', [line]))
        else:
            out.append(('other', [line]))
    return out

def style_name(st):
    return st[1][0].split()[1]

def set_props(st, props):
    """Sets key=value pairs on a style: replaced where the key is, added to the first line otherwise."""
    lines = list(st[1])
    for k, v in props.items():
        pat = re.compile(r'(?<=\s)' + re.escape(k) + r'=(?:"[^"]*"|\S+)')
        for i, l in enumerate(lines):
            if pat.search(l):
                lines[i] = pat.sub(f'{k}={v}', l, count=1)
                break
        else:
            first = lines[0]
            m = re.search(r'\s+use="', first)
            lines[0] = first[:m.start()] + f' {k}={v}' + first[m.start():] if m else first + f' {k}={v}'
    return ('style', lines)

def build(base, edits, extra_after_zone, head, settings, icons, guidance):
    sts = statements(base)
    out = []
    for st in sts:
        if st[0] == 'style' and style_name(st) in edits:
            st = set_props(st, edits[style_name(st)])
        out.append(st)
        if st[0] == 'style' and style_name(st) == 'zone':
            out += [('style', [l]) for l in extra_after_zone]
    body = '\n'.join(l for st in out for l in st[1]).rstrip('\n')
    lines = ['// ' + l for l in head] + [''] + settings + [''] + body.split('\n')
    lines += [f'guidance "{g}"' for g in guidance]
    lines += ['', '// ---- icons ' + '-' * 70] + icons
    return '\n'.join(lines) + '\n'

def colours(c):
    return [f'color {k.ljust(6)} {v}' for k, v in c.items()]

def fonts(sans):
    return [f'font sans  "{sans}" "{FONTS[sans]}"', 'font mono  "Geist Mono"', 'font serif "Newsreader"']

# the type of a group's name: the cloud's own diagrams label groups in plain sans, not spaced capitals
GROUP_TITLE = 'title.font=sans title.size=10 title.weight=600 title.spacing=0 title.caps=0'

def common_edits(radius, accent_tint, cloud_fill, cloud_stroke):
    return {
        # the cloud's icons are colour pictures; a little larger than the built-in outlines, still left of the text
        'node': {'radius': str(radius), 'icon.size': '24'},
        'focal': {'fill': accent_tint, 'stroke': 'accent', 'title.color': 'ink'},
        'terminal-focal': {'fill': accent_tint, 'title.color': 'ink'},
        'cloud': {'fill': cloud_fill, 'stroke': cloud_stroke},
        # on a white page the built-in grey cylinder is too heavy
        'store': {'fill': '#f5f6f7', 'stroke': 'ink/0.22'},
        'zone': {'radius': str(radius), 'fill': 'none', 'stroke': 'ink/0.35', 'title.font': 'sans', 'title.size': '10',
                 'title.weight': '600', 'title.color': 'ink', 'title.spacing': '0', 'title.caps': '0'},
    }

# ---- Azure ------------------------------------------------------------------------------------------------
def azure(base):
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#323130', 'muted': '#605e5c', 'soft': '#a19f9d',
         'accent': '#0078d4', 'link': '#0063b1', 'teal': '#008575', 'amber': '#c19c00', 'rose': '#d13438', 'violet': '#8661c5'}
    edits = common_edits(2, '#eff6fc', '#f3f9fd', 'accent/0.45')
    groups = [
        f'style subscription extends zone stroke=#ffb900 sw=1.2 {GROUP_TITLE} title.color=ink use="an Azure subscription; always give WxH"',
        f'style resource-group extends zone stroke=ink/0.45 dash=5,4 {GROUP_TITLE} title.color=ink use="a resource group; always give WxH"',
        f'style vnet extends zone fill=#0078d4/0.04 stroke=#0078d4 sw=1.2 {GROUP_TITLE} title.color=#0063b1 use="a virtual network; always give WxH"',
        f'style subnet extends zone fill=#0078d4/0.05 stroke=#0078d4/0.6 dash=4,3 {GROUP_TITLE} title.color=#0063b1 use="a subnet inside a virtual network; always give WxH"',
    ]
    head = ['Azure: FastDraw\'s built-in look in the colours of Azure\'s architecture diagrams. A white page, square cards,',
            'Azure blue for the subject and the main path, Open Sans, and Azure\'s own service icons (icon=app-service).',
            'Groups for a subscription, a resource group, a virtual network and a subnet. Same style names as the built-in look.']
    settings = ['canvas paper=paper dots=none', '', *colours(c), '', *fonts('Open Sans'), '',
                '// Azure\'s service icons, from Ben Coleman\'s icon collection (MIT) at a fixed commit, by their short names',
                'icondir "https://cdn.jsdelivr.net/gh/benc-uk/icon-collection@e33ee714d05a24a81cf6ccd967ef34b22cb77e65/azure-docs/{name}.svg"',
                'icons builtin=hidden']
    guidance = ['Icons are Azure\'s own, by short name: icon=app-service, functions, sql-database, cosmos-db, storage-accounts, key-vault, api-management, front-door, application-gateways, kubernetes-services, container-instances, service-bus, event-hubs, monitor, application-insights, virtual-machine. fastdraw icons <look> lists them all.',
                'Put resources in a vnet and subnets in it when the network matters; use resource-group or subscription for ownership.']
    return build(base, edits, groups, head, settings, [], guidance)

# ---- AWS --------------------------------------------------------------------------------------------------
# Short names for the services diagrams name most; every other icon is named from its file (AWSAppRunner -> app-runner).
AWS_SHORT = {
    'AmazonAPIGateway': 'api-gateway', 'AmazonAurora': 'aurora', 'AmazonAthena': 'athena', 'AmazonBedrock': 'bedrock',
    'AmazonCloudFront': 'cloudfront', 'AmazonCloudWatch': 'cloudwatch', 'AmazonCognito': 'cognito', 'AmazonDocumentDB': 'documentdb',
    'AmazonDynamoDB': 'dynamodb', 'AmazonEC2': 'ec2', 'AmazonEC2AutoScaling': 'ec2-auto-scaling', 'AmazonElasticBlockStore': 'ebs',
    'AmazonElasticContainerRegistry': 'ecr', 'AmazonElasticContainerService': 'ecs', 'AmazonElasticKubernetesService': 'eks',
    'AmazonEFS': 'efs', 'AmazonElastiCache': 'elasticache', 'AmazonEMR': 'emr', 'AmazonEventBridge': 'eventbridge',
    'AmazonKinesis': 'kinesis', 'AmazonKinesisDataStreams': 'kinesis-data-streams', 'AmazonDataFirehose': 'firehose',
    'AmazonManagedStreamingforApacheKafka': 'msk', 'AmazonMQ': 'mq', 'AmazonNeptune': 'neptune', 'AmazonOpenSearchService': 'opensearch',
    'AmazonRDS': 'rds', 'AmazonRedshift': 'redshift', 'AmazonRoute53': 'route53', 'AmazonSageMaker': 'sagemaker',
    'AmazonSimpleStorageService': 's3', 'AmazonSimpleStorageServiceGlacier': 's3-glacier', 'AmazonSimpleEmailService': 'ses',
    'AmazonSimpleNotificationService': 'sns', 'AmazonSimpleQueueService': 'sqs', 'AmazonVirtualPrivateCloud': 'vpc',
    'AmazonMemoryDB': 'memorydb', 'AmazonTimestream': 'timestream', 'AmazonQ': 'amazon-q', 'AmazonLightsail': 'lightsail',
    'AWSLambda': 'lambda', 'AWSFargate': 'fargate', 'AWSStepFunctions': 'step-functions', 'AWSIdentityandAccessManagement': 'iam',
    'AWSIAMIdentityCenter': 'iam-identity-center', 'AWSKeyManagementService': 'kms', 'AWSSecretsManager': 'secrets-manager',
    'AWSWAF': 'waf', 'AWSShield': 'shield', 'AWSCloudFormation': 'cloudformation', 'AWSCloudTrail': 'cloudtrail',
    'AWSCodePipeline': 'codepipeline', 'AWSCodeBuild': 'codebuild', 'AWSCodeDeploy': 'codedeploy', 'AWSCodeCommit': 'codecommit',
    'AWSAppRunner': 'app-runner', 'AWSAmplify': 'amplify', 'AWSAppSync': 'appsync', 'AWSBatch': 'batch', 'AWSBackup': 'backup',
    'AWSGlue': 'glue', 'AWSXRay': 'x-ray', 'ElasticLoadBalancing': 'elb', 'AWSTransitGateway': 'transit-gateway',
    'AWSDirectConnect': 'direct-connect', 'AWSCertificateManager': 'acm', 'AWSSystemsManager': 'systems-manager',
    'AWSOrganizations': 'organizations', 'AWSPrivateLink': 'privatelink', 'AWSGlobalAccelerator': 'global-accelerator',
    'AWSIoTCore': 'iot-core', 'AWSElasticBeanstalk': 'elastic-beanstalk', 'AWSDatabaseMigrationService': 'dms',
    'AWSDataSync': 'datasync', 'AWSTransferFamily': 'transfer-family', 'AWSSitetoSiteVPN': 'site-to-site-vpn',
    'AWSClientVPN': 'client-vpn', 'AWSNetworkFirewall': 'network-firewall', 'AWSConfig': 'config', 'AWSCloudMap': 'cloud-map',
    'AWSAppMesh': 'app-mesh', 'AWSOutpostsfamily': 'outposts', 'AWSSecurityHub': 'security-hub', 'AmazonGuardDuty': 'guardduty',
    'AmazonInspector': 'inspector', 'AmazonMacie': 'macie', 'AmazonManagedGrafana': 'grafana',
    'AmazonManagedServiceforPrometheus': 'prometheus', 'AmazonManagedWorkflowsforApacheAirflow': 'mwaa',
}

def kebab(file):
    s = re.sub(r'^(Amazon|AWS)(?=[A-Z])', '', file)
    s = s.replace('IoT', 'Iot').replace('FSx', 'Fsx').replace('rePost', 'Repost')
    words = re.findall(r'[A-Z]+\d*(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+\d*|[A-Z]+\d+|\d+', s)
    return '-'.join(w.lower() for w in words)

def aws_icons():
    files = [l.strip() for l in open(os.path.join(HERE, 'aws-icons.txt')) if l.strip()]
    names, out = {}, []
    for f in files:
        n = AWS_SHORT.get(f) or kebab(f)
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', n) or n in names:
            raise SystemExit(f'{f}: name {n!r} is not usable or is taken by {names.get(n)}')
        names[n] = f
    for n in sorted(names):
        out.append(f'icon {n} "https://cdn.jsdelivr.net/npm/aws-icons@3.3.0/icons/architecture-service/{names[n]}.svg"')
    return out

def aws(base):
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#232f3e', 'muted': '#545b64', 'soft': '#879196',
         'accent': '#ff9900', 'link': '#147eb4', 'teal': '#00a4a6', 'amber': '#d45b07', 'rose': '#dd344c', 'violet': '#8c4fff'}
    edits = common_edits(0, '#fff5e6', '#f2f8fc', 'link/0.45')
    # orange is a fill and a line colour; text in it is too light to read, so names stay ink and the main path's label darkens
    edits['primary'] = {'label.color': '#d45b07'}
    edits['kicker'] = {'color': '#d45b07'}
    groups = [
        f'style aws-cloud extends zone stroke=#232f3e sw=1.2 {GROUP_TITLE} title.color=#232f3e use="the AWS Cloud boundary; always give WxH"',
        f'style account extends zone stroke=#e7157b sw=1.2 {GROUP_TITLE} title.color=#e7157b use="an AWS account; always give WxH"',
        f'style region extends zone stroke=#00a4a6 dash=5,4 {GROUP_TITLE} title.color=#00a4a6 use="an AWS Region; always give WxH"',
        f'style az extends zone stroke=#00a4a6 dash=4,3 {GROUP_TITLE} title.color=#00a4a6 use="an Availability Zone; always give WxH"',
        f'style vpc extends zone stroke=#8c4fff sw=1.2 {GROUP_TITLE} title.color=#8c4fff use="a VPC; always give WxH"',
        f'style public-subnet extends zone fill=#7aa116/0.08 stroke=none {GROUP_TITLE} title.color=#5a7a10 use="a public subnet inside a VPC; always give WxH"',
        f'style private-subnet extends zone fill=#00a4a6/0.08 stroke=none {GROUP_TITLE} title.color=#00777a use="a private subnet inside a VPC; always give WxH"',
        f'style security-group extends zone stroke=#dd344c dash=3,3 {GROUP_TITLE} title.color=#dd344c use="a security group; always give WxH"',
    ]
    head = ['AWS: FastDraw\'s built-in look in the colours of AWS architecture diagrams. A white page, square cards, squid ink',
            'and AWS orange for the subject and the main path, Inter, and the AWS architecture icons (icon=lambda, icon=s3).',
            'Groups for the AWS Cloud, an account, a Region, an Availability Zone, a VPC, its subnets and a security group,',
            'in the colours AWS gives them. Same style names as the built-in look.']
    settings = ['canvas paper=paper dots=none', '', *colours(c), '', *fonts('Inter'), '',
                '// the AWS architecture service icons (the aws-icons package, at a fixed version), each named below',
                'icons builtin=hidden']
    guidance = ['Icons are the AWS architecture icons by short name: icon=lambda, s3, dynamodb, rds, aurora, ec2, ecs, eks, fargate, api-gateway, cloudfront, route53, elb, sqs, sns, eventbridge, step-functions, kinesis, cognito, iam, kms, secrets-manager, cloudwatch. Others are named from the service (app-runner, opensearch). fastdraw icons <look> lists them all.',
                'Nest groups the way AWS does: aws-cloud, then region, then vpc, then az, then public-subnet or private-subnet.']
    return build(base, edits, groups, head, settings, aws_icons(), guidance)

# ---- Google Cloud -----------------------------------------------------------------------------------------
GCP_RGB = ['apigee', 'cloudrun', 'computeengine', 'networking', 'secops']

def gcp(base):
    c = {'paper': '#ffffff', 'card': '#ffffff', 'ink': '#202124', 'muted': '#5f6368', 'soft': '#9aa0a6',
         'accent': '#1a73e8', 'link': '#188038', 'teal': '#129eaf', 'amber': '#e37400', 'rose': '#d93025', 'violet': '#9334e6'}
    edits = common_edits(8, '#e8f0fe', '#f1f8f3', 'link/0.45')
    # Google Cloud's diagrams draw groups as soft grey panels without an outline
    edits['zone'].update({'fill': '#f1f3f4', 'stroke': 'none', 'title.color': 'muted'})
    groups = [
        f'style google-cloud extends zone fill=none stroke=ink/0.4 sw=1.2 {GROUP_TITLE} title.color=ink use="the Google Cloud boundary; always give WxH"',
        f'style project extends zone fill=#f1f3f4 stroke=none {GROUP_TITLE} title.color=muted use="a Google Cloud project; always give WxH"',
        f'style region extends zone fill=#e8f0fe stroke=none {GROUP_TITLE} title.color=#1967d2 use="a region; always give WxH"',
        f'style vpc extends zone fill=none stroke=#1a73e8/0.6 dash=5,4 {GROUP_TITLE} title.color=#1967d2 use="a VPC network; always give WxH"',
        f'style on-premises extends zone fill=#fef7e0 stroke=none {GROUP_TITLE} title.color=#b06000 use="systems outside Google Cloud; always give WxH"',
    ]
    head = ['Google Cloud: FastDraw\'s built-in look in the colours of Google Cloud\'s architecture diagrams. A white page,',
            'rounded cards, Google blue for the subject and the main path, Roboto, soft grey panels for groups, and Google Cloud\'s',
            'product icons (icon=bigquery, icon=gke). Same style names as the built-in look.']
    base_url = 'https://cdn.jsdelivr.net/npm/gcp-icons@1.0.6/dist/icons/'
    settings = ['canvas paper=paper dots=none', '', *colours(c), '', *fonts('Roboto'), '',
                '// Google Cloud\'s product and category icons (the gcp-icons package, at a fixed version), by their names',
                f'icondir "{base_url}{{name}}-512-color.svg"', 'icons builtin=hidden']
    icons = [f'icon {n} "{base_url}{n}-512-color-rgb.svg"' for n in GCP_RGB]
    guidance = ['Icons are Google Cloud\'s, by name: icon=cloudrun, computeengine, gke, cloud-storage, cloudsql, cloudspanner, alloydb, bigquery, vertexai, apigee, looker, networking. The set has 45 product and category icons; fastdraw icons <look> lists them.',
                'Put a system in google-cloud, then project or region panels; on-premises holds what runs outside.']
    return build(base, edits, groups, head, settings, icons, guidance)

if __name__ == '__main__':
    base = open(os.path.join(HERE, 'base-styles.txt')).read().split('\n', 3)[3]  # without its two comment lines and the blank one
    for name, make in [('azure', azure), ('aws', aws), ('gcp', gcp)]:
        open(os.path.join(ROOT, name + '.look'), 'w').write(make(base))
    print('wrote azure.look, aws.look, gcp.look')
